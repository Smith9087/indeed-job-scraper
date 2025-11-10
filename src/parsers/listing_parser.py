from __future__ import annotations
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from .salary_parser import parse_salary_text
import re
from datetime import datetime, timezone

def _text(node) -> str:
    return re.sub(r"\s+", " ", (node.get_text(strip=True) if node else "")).strip()

def _float(text: str) -> Optional[float]:
    try:
        return float(text)
    except Exception:
        return None

def _parse_company_block(card) -> Dict[str, Any]:
    company = _text(card.select_one("[data-testid='company-name'], .companyName"))
    rating = _text(card.select_one("[data-testid='company-rating'], .ratingNumber"))
    review_count = _text(card.select_one("[data-testid='company-review-count'], .ratingCount"))
    logo = card.select_one("img[alt*=logo i], img[alt*=Logo i]")
    header = card.select_one("img[alt*=header i], img[alt*=Header i]")
    overview_link_el = card.select_one("a[href*='/cmp/']")
    return {
        "company": company or None,
        "companyBrandingAttributes": {
            "headerImageUrl": header.get("src") if header else None,
            "logoUrl": logo.get("src") if logo else None,
        },
        "companyOverviewLink": overview_link_el.get("href") if overview_link_el else None,
        "companyRating": _float(rating) if rating else None,
        "companyReviewCount": int(review_count.replace(",", "")) if review_count.isdigit() else None,
    }

def _parse_meta(card) -> Dict[str, Any]:
    display_title = _text(card.select_one("[data-testid='title'], h2.jobTitle"))
    title = display_title or None
    loc = _text(card.select_one("[data-testid='text-location'], .companyLocation"))
    snippet = _text(card.select_one("[data-testid='job-snippet'], .job-snippet"))
    link_el = card.select_one("a[href*='/rc/clk'], a[href*='/pagead/'], a[href*='/viewjob']")
    link = link_el.get("href") if link_el else None
    jobkey = None
    if link:
        m = re.search(r"[?&]jk=([0-9a-zA-Z]+)", link)
        if m:
            jobkey = m.group(1)
    # tags
    job_type_tags = [t.get_text(strip=True) for t in card.select("[data-testid='attribute-snippet'] span, .attribute_snippet")]
    # sponsored
    sponsored = bool(card.select_one("[data-testid='sponsored-label'], .sponsoredGray"))
    # new tag
    new_job = bool(card.select_one("[aria-label*='new' i], .new"))
    # relative time
    rel_time = _text(card.select_one("[data-testid='myJobsStateDate'], .date"))
    # possible remote tag
    remote_tokens = " ".join(job_type_tags + [snippet]).lower()
    remote_type = None
    if "remote" in remote_tokens and "hybrid" in remote_tokens:
        remote_type = "REMOTE_HYBRID"
    elif "remote" in remote_tokens:
        remote_type = "REMOTE"
    elif "hybrid" in remote_tokens:
        remote_type = "HYBRID"
    elif "onsite" in remote_tokens or "on-site" in remote_tokens:
        remote_type = "ONSITE"

    return {
        "displayTitle": title,
        "formattedLocation": loc or None,
        "snippet": snippet or None,
        "link": link,
        "viewJobLink": link,  # often the same on Indeed
        "jobkey": jobkey,
        "jobTypes": job_type_tags or [],
        "sponsored": sponsored,
        "newJob": new_job,
        "formattedRelativeTime": rel_time or None,
        "remoteWorkModel": {"type": remote_type} if remote_type else None,
    }

def parse_listings_from_html(html: str, source_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Best-effort parser for Indeed search result pages. Designed to be resilient to layout variants.
    """
    soup = BeautifulSoup(html, "lxml")
    result_cards = soup.select("[data-testid='result'], .result, .jobsearch-SerpJobCard")
    rows: List[Dict[str, Any]] = []

    # Fallback: some pages use a generic list container
    if not result_cards:
        result_cards = soup.select("li, article")

    for card in result_cards:
        meta = _parse_meta(card)
        company = _parse_company_block(card)

        # salary
        salary_text_node = card.select_one("[data-testid='attribute-salary'], .salary-snippet-container, .salary-snippet")
        salary_text = _text(salary_text_node)
        salary = parse_salary_text(salary_text) if salary_text else None
        # taxonomy attributes (labels/tiers)
        taxo_labels = [t.get_text(strip=True) for t in card.select("[data-testid='taxonomy-item'], .taxo")]
        taxonomy = [{"label": l, "tier": "tag"} for l in taxo_labels] if taxo_labels else None

        title = meta.get("displayTitle") or None
        link = meta.get("link")
        jobkey = meta.get("jobkey") or None

        row: Dict[str, Any] = {
            **company,
            **meta,
            "salarySnippet": {
                "text": salary_text or None,
                "currency": salary.get("currency") if salary else None,
            } if salary_text else None,
            "extractedSalary": salary or None,
            "title": title,
            "taxonomyAttributes": taxonomy,
            "expired": False,
            "locationCount": 1,
            "normTitle": _normalize_title(title) if title else None,
            "pubDate": _now_iso(),
            "sourceUrl": source_url,
        }

        rows.append(row)

    return rows

def _normalize_title(title: str) -> str:
    t = title.strip().lower()
    replacements = {
        "senior": "Sr",
        "jr.": "Jr",
        "junior": "Jr",
        "software developer": "Software Engineer",
    }
    for k, v in replacements.items():
        t = t.replace(k, v.lower())
    # Capitalize each word
    return " ".join(w.capitalize() for w in t.split())

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()