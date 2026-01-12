from utils.file_handler import load_sales_data
from utils.api_handler import fetch_product_info
from utils.data_processor import (
    compute_revenue_per_category,
    top_selling_product,
    sales_distribution_by_region,
)


def main() -> None:
    file_path = r"data\sales_data.txt"
    valid_records, total_parsed, invalid_removed = load_sales_data(file_path)

    print("=== Sales Data Load Summary ===")
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_removed}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    # --- Analytics ---
    revenue_by_category = compute_revenue_per_category(valid_records)
    top_product, top_qty = top_selling_product(valid_records)
    region_distribution = sales_distribution_by_region(valid_records)

    print("\n=== Analytics Results ===")

    print("\n1) Total Revenue per Category:")
    for cat, rev in sorted(revenue_by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {rev:.2f}")

    print("\n2) Top-Selling Product (by quantity):")
    print(f"  {top_product} (Total Qty: {top_qty})")

    print("\n3) Region-wise Sales Distribution (% of revenue):")
    for region, pct in sorted(region_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {pct:.2f}%")

    # --- API Demo (Real-time product info) ---
    print("\n=== API Demo (DummyJSON) ===")
    sample_product_id = "P101"
    info = fetch_product_info(sample_product_id)

    if info is None:
        print(f"Could not fetch product info for {sample_product_id} (ID may not exist on DummyJSON).")
    else:
        # Print a few useful fields
        print(f"Product API result for {sample_product_id}:")
        print(f"  title: {info.get('title')}")
        print(f"  brand: {info.get('brand')}")
        print(f"  category: {info.get('category')}")
        print(f"  price: {info.get('price')}")
        print(f"  rating: {info.get('rating')}")
    # --- Save output report ---
    report_lines = []
    report_lines.append("=== Sales Data Load Summary ===")
    report_lines.append(f"Total records parsed: {total_parsed}")
    report_lines.append(f"Invalid records removed: {invalid_removed}")
    report_lines.append(f"Valid records after cleaning: {len(valid_records)}")
    report_lines.append("")
    report_lines.append("=== Analytics Results ===")
    report_lines.append("1) Total Revenue per Category:")
    for cat, rev in sorted(revenue_by_category.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"  {cat}: {rev:.2f}")
    report_lines.append("")
    report_lines.append("2) Top-Selling Product (by quantity):")
    report_lines.append(f"  {top_product} (Total Qty: {top_qty})")
    report_lines.append("")
    report_lines.append("3) Region-wise Sales Distribution (% of revenue):")
    for region, pct in sorted(region_distribution.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"  {region}: {pct:.2f}%")
    report_lines.append("")
    report_lines.append("=== API Demo (DummyJSON) ===")
    if info is None:
        report_lines.append("API fetch failed or product not found.")
    else:
        report_lines.append(f"Product API result for {sample_product_id}:")
        report_lines.append(f"  title: {info.get('title')}")
        report_lines.append(f"  brand: {info.get('brand')}")
        report_lines.append(f"  category: {info.get('category')}")
        report_lines.append(f"  price: {info.get('price')}")
        report_lines.append(f"  rating: {info.get('rating')}")

    output_path = r"output\analysis_report.txt"
    write_report(output_path, report_lines)
    print(f"\nReport saved to: {output_path}")


def write_report(path: str, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
