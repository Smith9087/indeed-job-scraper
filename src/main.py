import argparse
import csv
import json
import logging
import sys
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional

# Put src/ on sys.path so implicit namespace packages (parsers, crawler, exporters) are importable.
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from crawler.pagination import build_pagination_urls
from crawler.throttling import RateLimiter, backoff
from exporters.json_exporter import JsonExporter
from exporters.csv_exporter import CsvExporter
from parsers.listing_parser import parse_listings_from_html
from dateutil import tz
import requests

def read_settings(settings_path: Optional[Path]) -> Dict[str, Any]:
    defaults = {
        "output_format": "json",
        "output_path": "output.json",
        "max_results": 100,
        "concurrency": 1,
        "requests_per_minute": 30,
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "timeout_seconds": 20,
    }
    if settings_path and settings_path.exists():
        try:
            with settings_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                defaults.update({k: v for k, v in data.items() if v is not None})
        except Exception as e:
            logging.warning("Failed to read settings file %s: %s", settings_path, e)
    return defaults

def load_input_urls(input_arg: Optional[str], inputs_file: Optional[Path]) -> List[str]:
    urls: List[str] = []
    if input_arg:
        urls.append(input_arg.strip())
    if inputs_file and inputs_file.exists():
        with inputs_file.open("r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith("#"):
                    urls.append(s)
    # Deduplicate while preserving order
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            uniq.append(u)
            seen.add(u)
    return uniq

def fetch(session: requests.Session, url: str, timeout: int) -> Optional[str]:
    try:
        if url.startswith("file://"):
            path = Path(url[7:])
            return path.read_text(encoding="utf-8")
        elif url.startswith("/") or (":" not in url and Path(url).exists()):
            # Local path
            return Path(url).read_text(encoding="utf-8")
        else:
            resp = session.get(url, timeout=timeout)
            if 200 <= resp.status_code < 300:
                return resp.text
            logging.warning("HTTP %s from %s", resp.status_code, url)
            return None
    except Exception as e:
        logging.error("Fetch error for %s: %s", url, e)
        return None

def export_results(rows: List[Dict[str, Any]], fmt: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if fmt.lower() == "json":
        JsonExporter(out_path).write(rows)
    elif fmt.lower() in ("csv", "tsv"):
        dialect = "excel" if fmt.lower() == "csv" else "excel-tab"
        CsvExporter(out_path, dialect=dialect).write(rows)
    else:
        raise ValueError(f"Unsupported output format: {fmt}")

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Indeed Job Scraper — extract structured listings from Indeed search pages.")
    parser.add_argument("--url", help="Indeed search URL (can be provided multiple times)", action="append")
    parser.add_argument("--inputs", type=str, default=str(Path(__file__).parents[1] / "data" / "inputs.sample.txt"),
                        help="Path to a text file with one URL per line.")
    parser.add_argument("--settings", type=str,
                        default=str(Path(__file__).parent / "config" / "settings.example.json"),
                        help="Path to settings JSON.")
    parser.add_argument("--max-results", type=int, help="Maximum number of listings to extract.")
    parser.add_argument("--format", choices=["json", "csv", "tsv"], help="Output format.")
    parser.add_argument("--out", type=str, help="Output file path.")
    parser.add_argument("--pages", type=int, default=None,
                        help="Override number of pages to crawl (auto by max-results if omitted).")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR).")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    settings = read_settings(Path(args.settings) if args.settings else None)

    fmt = (args.format or settings["output_format"]).lower()
    output_path = Path(args.out or settings["output_path"])
    max_results = args.max_results or int(settings["max_results"])
    requests_per_minute = int(settings["requests_per_minute"])
    timeout_seconds = int(settings["timeout_seconds"])
    user_agent = settings["user_agent"]

    # Load URLs
    urls: List[str] = []
    if args.url:
        urls.extend(args.url)
    urls = load_input_urls(None, Path(args.inputs)) if not urls else urls
    if not urls:
        logging.error("No input URLs provided. Use --url or provide a file in data/inputs.sample.txt.")
        return 2

    limiter = RateLimiter(max_calls=requests_per_minute, per_seconds=60.0)

    session = requests.Session()
    session.headers.update({
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })

    all_rows: List[Dict[str, Any]] = []
    for base_url in urls:
        pages = args.pages
        to_fetch: Iterable[str] = build_pagination_urls(base_url, max_results=max_results, max_pages=pages)
        for page_url in to_fetch:
            if len(all_rows) >= max_results:
                break
            limiter.acquire()
            html = backoff(lambda: fetch(session, page_url, timeout_seconds), tries=3, first_delay=1.5)
            if not html:
                continue
            rows = parse_listings_from_html(html, source_url=page_url)
            for r in rows:
                all_rows.append(r)
                if len(all_rows) >= max_results:
                    break
        if len(all_rows) >= max_results:
            break

    # Dedup by jobkey where present
    seen_keys = set()
    deduped: List[Dict[str, Any]] = []
    for r in all_rows:
        key = r.get("jobkey") or r.get("link")
        if key and key in seen_keys:
            continue
        if key:
            seen_keys.add(key)
        deduped.append(r)

    export_results(deduped[:max_results], fmt=fmt, out_path=output_path)
    logging.info("Exported %d rows to %s", min(len(deduped), max_results), output_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())