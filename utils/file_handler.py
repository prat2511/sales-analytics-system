from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class SalesRecord:
    order_id: str
    product: str
    category: str
    quantity: int
    price: float
    country: str


def _parse_line(line: str) -> SalesRecord | None:
    """
    Expected pipe-delimited format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
    """
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) != 8:
        return None

    txn_id, date_s, product_id, product_name, qty_s, price_s, customer_id, region = parts

    # Transaction ID must start with T
    if not txn_id or not txn_id.startswith("T"):
        return None

    # CustomerID and Region are mandatory
    if not customer_id or not region:
        return None

    # Clean product name (remove commas)
    product_name = product_name.replace(",", "").strip()

    # Clean numeric formatting (remove commas)
    qty_s = qty_s.replace(",", "").strip()
    price_s = price_s.replace(",", "").strip()

    try:
        quantity = int(qty_s)
        price = float(price_s)
        if quantity <= 0 or price <= 0:
            return None
    except ValueError:
        return None

    return SalesRecord(
        order_id=txn_id,
        product=product_name,
        category=product_id,
        quantity=quantity,
        price=price,
        country=region,
    )


def load_sales_data(file_path: str | Path) -> Tuple[List[SalesRecord], int, int]:
    """
    Loads and validates sales data from a text file.

    Returns:
        valid_records,
        total_records_parsed,
        invalid_records_removed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [ln for ln in lines if ln.strip()]

    # Skip header if present
    if lines and lines[0].lower().startswith("transaction"):
        lines = lines[1:]

    total_parsed = len(lines)
    valid: List[SalesRecord] = []
    invalid = 0

    for ln in lines:
        rec = _parse_line(ln)
        if rec is None:
            invalid += 1
        else:
            valid.append(rec)

    return valid, total_parsed, invalid
