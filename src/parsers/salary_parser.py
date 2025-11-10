from __future__ import annotations
import re
from typing import Optional, Dict

_CURRENCY_MAP = {
    "$": "USD",
    "£": "GBP",
    "€": "EUR",
    "₹": "INR",
    "C$": "CAD",
    "A$": "AUD",
    "CA$": "CAD",
    "AU$": "AUD",
    "PKR": "PKR",
}

def _detect_currency(text: str) -> Optional[str]:
    for sym, code in _CURRENCY_MAP.items():
        if sym in text:
            return code
    # Try ISO code pattern
    m = re.search(r"\b([A-Z]{3})\b", text)
    if m:
        return m.group(1)
    return None

def parse_salary_text(text: str) -> Optional[Dict]:
    """
    Parse salary snippet like "$140,000 - $170,000 a year" into min/max/type/currency.
    Returns None if no numeric values are present.
    """
    if not text or not re.search(r"\d", text):
        return None

    currency = _detect_currency(text)

    # Extract numbers possibly containing commas/decimals
    nums = [n.replace(",", "") for n in re.findall(r"(?<!\d)(\d{1,3}(?:,\d{3})*(?:\.\d+)?)", text)]
    values = []
    for n in nums:
        try:
            values.append(float(n))
        except Exception:
            pass
    if not values:
        return None

    # Detect cadence
    cadence = None
    lowered = text.lower()
    for k, v in {
        "per year": "yearly",
        "a year": "yearly",
        "year": "yearly",
        "per month": "monthly",
        "a month": "monthly",
        "month": "monthly",
        "per hour": "hourly",
        "an hour": "hourly",
        "hour": "hourly",
        "per day": "daily",
        "a day": "daily",
        "day": "daily",
    }.items():
        if k in lowered:
            cadence = v
            break

    min_val = min(values)
    max_val = max(values)
    if len(values) == 1:
        max_val = min_val

    return {
        "min": min_val,
        "max": max_val,
        "type": cadence,
        "currency": currency,
    }