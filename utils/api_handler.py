from __future__ import annotations

import json
import re
import urllib.request
from typing import Any, Dict, Optional


def _extract_numeric_id(product_id: str) -> Optional[int]:
    """
    Converts IDs like 'P101' -> 101 for DummyJSON.
    """
    match = re.search(r"(\d+)", product_id)
    if not match:
        return None
    return int(match.group(1))


def fetch_product_info(product_id: str, timeout_sec: int = 10) -> Optional[Dict[str, Any]]:
    """
    Fetch product info from DummyJSON API.

    Example:
      P101 -> https://dummyjson.com/products/101
    """
    numeric_id = _extract_numeric_id(product_id)
    if numeric_id is None:
        return None

    url = f"https://dummyjson.com/products/{numeric_id}"

    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as response:
            if response.status != 200:
                return None
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except Exception:
        return None
