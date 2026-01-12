from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from utils.file_handler import SalesRecord


def compute_revenue_per_category(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Revenue per category.
    Revenue = quantity * price.
    """
    revenue_by_cat: Dict[str, float] = defaultdict(float)
    for r in records:
        revenue_by_cat[r.category] += r.quantity * r.price
    return dict(revenue_by_cat)


def top_selling_product(records: List[SalesRecord]) -> Tuple[str, int]:
    """
    Returns (product_name, total_quantity_sold) for the top-selling product by quantity.
    """
    qty_by_product: Dict[str, int] = defaultdict(int)
    for r in records:
        qty_by_product[r.product] += r.quantity

    if not qty_by_product:
        return ("", 0)

    top_product = max(qty_by_product.items(), key=lambda x: x[1])
    return top_product[0], top_product[1]


def sales_distribution_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Region-wise sales distribution (share of total revenue by region).
    Output: {region: percentage_of_total_revenue}
    """
    revenue_by_region: Dict[str, float] = defaultdict(float)
    total_revenue = 0.0

    for r in records:
        rev = r.quantity * r.price
        revenue_by_region[r.country] += rev
        total_revenue += rev

    if total_revenue == 0:
        return {k: 0.0 for k in revenue_by_region}

    return {k: (v / total_revenue) * 100 for k, v in revenue_by_region.items()}
