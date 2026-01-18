from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Any, Tuple

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)


def _fmt_money(x: float) -> str:
    return f"₹{x:,.2f}"


def _line(char: str = "=", n: int = 44) -> str:
    return char * n


def generate_sales_report(
    transactions: List[Dict[str, Any]],
    enriched_transactions: List[Dict[str, Any]],
    output_file: str = r"output\sales_report.txt",
) -> None:
    """
    Generates a comprehensive formatted text report (8 sections, in order).
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records_processed = len(transactions)

    # Overall metrics
    total_revenue = calculate_total_revenue(transactions)
    total_tx = len(transactions)
    avg_order_value = (total_revenue / total_tx) if total_tx else 0.0

    dates = sorted({t.get("date", "") for t in transactions if t.get("date")})
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # Region stats
    reg_stats = region_wise_sales(transactions)

    # Top products
    top_products = top_selling_products(transactions, n=5)

    # Top customers (convert customer_analysis dict to ranked list)
    cust_stats = customer_analysis(transactions)
    top_customers = []
    rank = 1
    for cid, info in cust_stats.items():
        top_customers.append((rank, cid, info["total_spent"], info["purchase_count"]))
        rank += 1
        if rank > 5:
            break

    # Daily trend
    daily = daily_sales_trend(transactions)

    # Product performance
    peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions, threshold=10)

    # Avg transaction value per region
    avg_tx_value_region = {}
    for reg, info in reg_stats.items():
        cnt = info["transaction_count"]
        avg_tx_value_region[reg] = (info["total_sales"] / cnt) if cnt else 0.0

    # API enrichment summary
    enriched_count = 0
    failed_products = set()
    for t in enriched_transactions:
        if t.get("API_Match") is True:
            enriched_count += 1
        else:
            # collect product IDs that failed enrichment
            pid = t.get("product_id") or t.get("ProductID")
            if pid:
                failed_products.add(pid)

    success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0.0

    # ------------------- WRITE REPORT -------------------
    lines: List[str] = []

    # 1. HEADER
    lines.append(_line("="))
    lines.append("       SALES ANALYTICS REPORT")
    lines.append(f"     Generated: {now}")
    lines.append(f"     Records Processed: {records_processed}")
    lines.append(_line("="))
    lines.append("")

    # 2. OVERALL SUMMARY
    lines.append("OVERALL SUMMARY")
    lines.append(_line("-"))
    lines.append(f"Total Revenue:        {_fmt_money(total_revenue)}")
    lines.append(f"Total Transactions:   {total_tx}")
    lines.append(f"Average Order Value:  {_fmt_money(avg_order_value)}")
    lines.append(f"Date Range:           {date_range}")
    lines.append("")

    # 3. REGION-WISE PERFORMANCE
    lines.append("REGION-WISE PERFORMANCE")
    lines.append(_line("-"))
    lines.append(f"{'Region':<8}{'Sales':>15}{'% of Total':>12}{'Txns':>8}")
    for reg, info in reg_stats.items():
        lines.append(
            f"{reg:<8}"
            f"{_fmt_money(info['total_sales']):>15}"
            f"{(str(info['percentage']) + '%'):>12}"
            f"{info['transaction_count']:>8}"
        )
    lines.append("")

    # 4. TOP 5 PRODUCTS
    lines.append("TOP 5 PRODUCTS")
    lines.append(_line("-"))
    lines.append(f"{'Rank':<6}{'Product Name':<22}{'Qty':>8}{'Revenue':>15}")
    for i, (name, qty, rev) in enumerate(top_products, start=1):
        lines.append(f"{i:<6}{name:<22}{qty:>8}{_fmt_money(rev):>15}")
    lines.append("")

    # 5. TOP 5 CUSTOMERS
    lines.append("TOP 5 CUSTOMERS")
    lines.append(_line("-"))
    lines.append(f"{'Rank':<6}{'Customer':<12}{'Total Spent':>15}{'Orders':>8}")
    for r, cid, spent, cnt in top_customers:
        lines.append(f"{r:<6}{cid:<12}{_fmt_money(spent):>15}{cnt:>8}")
    lines.append("")

    # 6. DAILY SALES TREND
    lines.append("DAILY SALES TREND")
    lines.append(_line("-"))
    lines.append(f"{'Date':<12}{'Revenue':>15}{'Txns':>8}{'Customers':>12}")
    for d, info in daily.items():
        lines.append(
            f"{d:<12}"
            f"{_fmt_money(info['revenue']):>15}"
            f"{info['transaction_count']:>8}"
            f"{info['unique_customers']:>12}"
        )
    lines.append("")

    # 7. PRODUCT PERFORMANCE ANALYSIS
    lines.append("PRODUCT PERFORMANCE ANALYSIS")
    lines.append(_line("-"))
    lines.append(f"Best selling day: {peak_date} | Revenue: {_fmt_money(peak_revenue)} | Transactions: {peak_count}")
    lines.append("")
    lines.append("Low performing products (qty < 10):")
    if low_products:
        for name, qty, rev in low_products:
            lines.append(f"  - {name}: qty={qty}, revenue={_fmt_money(rev)}")
    else:
        lines.append("  - None")
    lines.append("")
    lines.append("Average transaction value per region:")
    for reg, val in sorted(avg_tx_value_region.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  - {reg}: {_fmt_money(val)}")
    lines.append("")

    # 8. API ENRICHMENT SUMMARY
    lines.append("API ENRICHMENT SUMMARY")
    lines.append(_line("-"))
    lines.append(f"Total transactions enriched: {enriched_count} / {len(enriched_transactions)}")
    lines.append(f"Success rate: {success_rate:.2f}%")
    lines.append("Products that could not be enriched:")
    if failed_products:
        for pid in sorted(failed_products):
            lines.append(f"  - {pid}")
    else:
        lines.append("  - None")
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
