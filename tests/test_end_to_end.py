import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

# Make src/ importable
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from parsers.listing_parser import parse_listings_from_html
from exporters.json_exporter import JsonExporter
from exporters.csv_exporter import CsvExporter

def _sample_html() -> str:
    return """
    <html><body>
      <div data-testid="result">
        <h2 class="jobTitle">Backend Engineer</h2>
        <span data-testid="company-name">Beta LLC</span>
        <span data-testid="text-location">Remote</span>
        <div data-testid="job-snippet">APIs and microservices</div>
        <a href="https://www.indeed.com/viewjob?jk=xyz789">View</a>
        <div class="salary-snippet">$60 - $80 an hour</div>
        <span data-testid="attribute-snippet"><span>Contract</span></span>
        <span aria-label="new">New</span>
      </div>
      <div data-testid="result">
        <h2 class="jobTitle">Frontend Developer</h2>
        <span data-testid="company-name">Gamma Inc</span>
        <span data-testid="text-location">London, UK</span>
        <div data-testid="job-snippet">React/TypeScript</div>
        <a href="https://www.indeed.com/viewjob?jk=uvw000">View</a>
        <div data-testid="attribute-salary">£50,000 - £65,000 a year</div>
        <span data-testid="attribute-snippet"><span>Full-time</span></span>
      </div>
    </body></html>
    """

def test_end_to_end_exporters_write_files(tmp_path: Path):
    html = _sample_html()
    rows = parse_listings_from_html(html, source_url="https://example.com/search")
    assert len(rows) == 2

    out_json = tmp_path / "jobs.json"
    out_csv = tmp_path / "jobs.csv"

    JsonExporter(out_json).write(rows)
    CsvExporter(out_csv).write(rows)

    assert out_json.exists() and out_json.stat().st_size > 0
    assert out_csv.exists() and out_csv.stat().st_size > 0

    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) == 2
    keys = set(data[0].keys())
    assert "title" in keys and "company" in keys and "link" in keys