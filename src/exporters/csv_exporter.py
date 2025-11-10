from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Dict, Any

_FLAT_COLUMNS = [
    "company",
    "companyBrandingAttributes.headerImageUrl",
    "companyBrandingAttributes.logoUrl",
    "companyOverviewLink",
    "companyRating",
    "companyReviewCount",
    "displayTitle",
    "expired",
    "extractedSalary.min",
    "extractedSalary.max",
    "extractedSalary.type",
    "extractedSalary.currency",
    "formattedLocation",
    "formattedRelativeTime",
    "jobLocationCity",
    "jobLocationState",
    "jobTypes",
    "jobkey",
    "link",
    "locationCount",
    "newJob",
    "normTitle",
    "pubDate",
    "remoteWorkModel.type",
    "salarySnippet.text",
    "salarySnippet.currency",
    "snippet",
    "sponsored",
    "title",
    "urgentlyHiring",
    "viewJobLink",
    "sourceUrl",
]

def _get(d: Dict[str, Any], dotted: str):
    cur = d
    parts = dotted.split(".")
    for p in parts:
        if cur is None:
            return None
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    if isinstance(cur, list):
        return "|".join(map(str, cur))
    return cur

class CsvExporter:
    def __init__(self, path: Path, dialect: str = "excel"):
        self.path = Path(path)
        self.dialect = dialect

    def write(self, rows: List[Dict[str, Any]]) -> None:
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_FLAT_COLUMNS, dialect=self.dialect)
            writer.writeheader()
            for r in rows:
                flat = {col: _get(r, col) for col in _FLAT_COLUMNS}
                writer.writerow(flat)