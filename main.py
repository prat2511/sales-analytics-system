# main.py (Complete, clean, exam-safe version — dictionaries + validation + Task 2.1/2.2/2.3 + API + report)

from utils.file_handler import load_sales_data, validate_and_filter
from utils.api_handler import fetch_product_info
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)


def write_report(path: str, lines: list[str]) -> None:
    """Writes report lines to a text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    file_path = r"data\sales_data.txt"

    # load_sales_data returns: (transactions_list, total_parsed, invalid_removed_by_parser)
    transactions, total_parsed, invalid_removed = load_sales_data(file_path)

    print("=== Sales Data Load Summary ===")
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed (parsing stage): {invalid_removed}")
    print(f"Records returned from loader: {len(transactions)}")

    # ------------------------------
    # Task 1.3: Validation + Filtering
    # ------------------------------
    filtered_transactions, invalid_count, filter_summary = validate_and_filter(
        transactions,
        region=None,
        min_amount=None,
        max_amount=None,
    )

    print("\n=== Validation & Filter Summary (Task 1.3) ===")
    print(f"Invalid transactions (validation stage): {invalid_count}")
    print("Filter summary:")
    print(filter_summary)

    # IMPORTANT: From this point, use ONLY validated+filtered data
    valid_records = filtered_transactions

    # ------------------------------
    # Part 2: Data Processing (Task 2.1, 2.2, 2.3)
    # ------------------------------
    total_revenue = calculate_total_revenue(valid_records)
    region_stats = region_wise_sales(valid_records)
    top_products = top_selling_products(valid_records, n=5)
    customer_stats = customer_analysis(valid_records)
    daily_trend = daily_sales_trend(valid_records)
    peak_day = find_peak_sales_day(valid_records)
    low_products = low_performing_products(valid_records, threshold=10)

    print("\n=== Part 2 Outputs ===")
    print(f"Total Revenue: {total_revenue:.2f}")
    print("\nRegion-wise Sales:")
    for reg, stats in region_stats.items():
	    print(f"  {reg}: total_sales={stats['total_sales']:.2f}, "
		    f"transactions={stats['transaction_count']}, "
			f"percentage={stats['percentage']:.2f}%")

    print("\nTop Selling Products (Top 5):")
    for name, qty, rev in top_products:
	    print(f"  {name}: qty={qty}, revenue={rev:.2f}")

    print("\nPeak Sales Day:")
    print(f"  date={peak_day[0]}, revenue={peak_day[1]:.2f}, transactions={peak_day[2]}")

    print("\nLow Performing Products (<10 qty):")
    for name, qty, rev in low_products:
	    print(f"  {name}: qty={qty}, revenue={rev:.2f}")


    # ------------------------------
    # API Demo (DummyJSON)
    # ------------------------------
    print("\n=== API Demo (DummyJSON) ===")
    sample_product_id = "P101"
    info = fetch_product_info(sample_product_id)

    if info is None:
        print(f"Could not fetch product info for {sample_product_id}.")
    else:
        print(f"Product API result for {sample_product_id}:")
        print(f"  title: {info.get('title')}")
        print(f"  brand: {info.get('brand')}")
        print(f"  category: {info.get('category')}")
        print(f"  price: {info.get('price')}")
        print(f"  rating: {info.get('rating')}")

    # ------------------------------
    # Save output report
    # ------------------------------
    report_lines: list[str] = []

    report_lines.append("=== Sales Data Load Summary ===")
    report_lines.append(f"Total records parsed: {total_parsed}")
    report_lines.append(f"Invalid records removed (parsing stage): {invalid_removed}")
    report_lines.append(f"Records returned from loader: {len(transactions)}")
    report_lines.append("")

    report_lines.append("=== Validation & Filter Summary (Task 1.3) ===")
    report_lines.append(str(filter_summary))
    report_lines.append("")

    report_lines.append("=== Part 2 Outputs ===")
    report_lines.append(f"Total Revenue: {total_revenue:.2f}")
    report_lines.append("")
	
    report_lines.append("Region-wise Sales:")
    for reg, stats in region_stats.items():
	    report_lines.append(
            f"  {reg}: total_sales={stats['total_sales']:.2f}, "
            f"transactions={stats['transaction_count']}, "
            f"percentage={stats['percentage']:.2f}%"
        )
    report_lines.append("")
    report_lines.append("Top Selling Products (Top 5):")
    for name, qty, rev in top_products:
	    report_lines.append(f"  {name}: qty={qty}, revenue={rev:.2f}")
    report_lines.append("")
	
    report_lines.append("Peak Sales Day:")
    report_lines.append(f"  date={peak_day[0]}, revenue={peak_day[1]:.2f}, transactions={peak_day[2]}")
    report_lines.append("")
	
    report_lines.append("Low Performing Products (<10 qty):")
    for name, qty, rev in low_products:
	    report_lines.append(f"  {name}: qty={qty}, revenue={rev:.2f}")
    report_lines.append("")

    report_lines.append("=== API Demo (DummyJSON) ===")
    if info is None:
        report_lines.append(f"Could not fetch product info for {sample_product_id}.")
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


if __name__ == "__main__":
    main()
