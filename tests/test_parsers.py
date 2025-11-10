import sys
from pathlib import Path

# Ensure src/ is importable
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from parsers.salary_parser import parse_salary_text
from parsers.listing_parser import parse_listings_from_html

def test_parse_salary_text_range_yearly():
    s = "$140,000 - $170,000 a year"
    parsed = parse_salary_text(s)
    assert parsed is not None
    assert parsed["min"] == 140000.0
    assert parsed["max"] == 170000.0
    assert parsed["type"] == "yearly"
    assert parsed["currency"] == "USD"

def test_parse_salary_text_hourly_single_value():
    s = "£20 an hour"
    parsed = parse_salary_text(s)
    assert parsed["min"] == 20.0
    assert parsed["max"] == 20.0
    assert parsed["type"] == "hourly"
    assert parsed["currency"] == "GBP"

def test_parse_listings_from_html_minimal_card():
    html = """
    <html><body>
      <div data-testid="result">
        <h2 class="jobTitle">Senior Data Engineer</h2>
        <span data-testid="company-name">Acme Corp</span>
        <span data-testid="text-location">New York, NY</span>
        <div data-testid="job-snippet">Build pipelines</div>
        <a href="https://www.indeed.com/viewjob?jk=abc123">View</a>
        <div data-testid="attribute-salary">$140,000 - $170,000 a year</div>
        <span data-testid="attribute-snippet"><span>Full-time</span></span>
        <span data-testid="myJobsStateDate">3 days ago</span>
      </div>
    </body></html>
    """
    rows = parse_listings_from_html(html, source_url="https://example.com/page")
    assert len(rows) == 1
    row = rows[0]
    assert row["company"] == "Acme Corp"
    assert row["title"] == "Senior Data Engineer"
    assert row["formattedLocation"] == "New York, NY"
    assert row["extractedSalary"]["min"] == 140000.0
    assert row["jobkey"] == "abc123"
    assert row["sourceUrl"] == "https://example.com/page"