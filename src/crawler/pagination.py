from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from typing import Iterable, List, Optional

def _with_query_param(url: str, **params) -> str:
    """
    Return URL with updated/added query parameters.
    """
    parts = list(urlparse(url))
    q = dict(parse_qsl(parts[4], keep_blank_values=True))
    q.update({k: str(v) for k, v in params.items() if v is not None})
    parts[4] = urlencode(q, doseq=True)
    return urlunparse(parts)

def build_pagination_urls(base_url: str, max_results: int = 100, page_size: int = 15,
                          max_pages: Optional[int] = None) -> Iterable[str]:
    """
    Indeed typically paginates using 'start' query parameter (0, 10, 20, ...).
    We default to a conservative page_size (15). Caller can override.

    :param base_url: The Indeed search URL (can include filters).
    :param max_results: Maximum number of items desired.
    :param page_size: Estimated number of items per page.
    :param max_pages: Optional hard cap on the number of pages to produce.
    :return: Iterable of URLs for each page.
    """
    # Respect explicit 'start' if present for the first page; otherwise start=0
    num_pages = (max_results + page_size - 1) // page_size
    if max_pages is not None:
        num_pages = min(num_pages, max_pages)

    for i in range(num_pages):
        start = i * page_size
        yield _with_query_param(base_url, start=start)