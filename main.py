from utils.file_handler import load_sales_data, validate_and_filter
from utils.api_handler import (
    fetch_all_products,
    fetch_products_101_to_200,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data,
)
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)
from utils.report_generator import generate_sales_report


def _banner() -> None:
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)
    print("")


def main() -> None:
    """
    Main execution function (Task 5.1)
    """
    try:
        _banner()

        # [1/10] Reading sales data
        print("[1/10] Reading sales data...")
        file_path = r"data\sales_data.txt"
        transactions, total_parsed, invalid_removed_parse = load_sales_data(file_path)
        print(f"✓ Successfully read {total_parsed} transactions")
        if invalid_removed_parse:
            print(f"  (Removed during parsing: {invalid_removed_parse})")
        print("")

        # [2/10] Parsing and cleaning data
        # (Already handled in load_sales_data + parser)
        print("[2/10] Parsing and cleaning data...")
        print(f"✓ Parsed {len(transactions)} records")
        print("")

        # [3/10] Filter options (show regions + amount range)
        print("[3/10] Filter Options Available:")

        # Use validate_and_filter once to compute available regions/range prints,
        # but do not filter yet. This prints regions + amount range as required.
        _tmp_valid, _tmp_invalid, _tmp_summary = validate_and_filter(transactions)

        # Ask user if they want filtering
        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        region = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region_in = input("Enter region (or press Enter to skip): ").strip()
            if region_in:
                region = region_in

            min_in = input("Enter minimum amount (or press Enter to skip): ").strip()
            if min_in:
                min_amount = float(min_in)

            max_in = input("Enter maximum amount (or press Enter to skip): ").strip()
            if max_in:
                max_amount = float(max_in)

        print("")

        # [4/10] Validating transactions (and applying optional filters)
        print("[4/10] Validating transactions...")
        valid_records, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount,
        )
        print(f"✓ Valid: {len(valid_records)} | Invalid: {invalid_count}")
        print("")

        # [5/10] Analyzing sales data (Part 2)
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_records)
        region_stats = region_wise_sales(valid_records)
        top_products = top_selling_products(valid_records, n=5)
        cust_stats = customer_analysis(valid_records)
        daily_trend = daily_sales_trend(valid_records)
        peak_day = find_peak_sales_day(valid_records)
        low_products = low_performing_products(valid_records, threshold=10)
        print("✓ Analysis complete")
        print("")

        # [6/10] Fetching product data from API (Task 3.1a)
        print("[6/10] Fetching product data from API...")
        api_products_100 = fetch_all_products()  # limit=100 (required)
        print(f"✓ Fetched {len(api_products_100)} products (limit=100)")
        print("")

        # [7/10] Enriching sales data (two outputs)
        print("[7/10] Enriching sales data...")

        mapping_100 = create_product_mapping(api_products_100)
        enriched_100 = enrich_sales_data(valid_records, mapping_100)

        # Supplemental 101-200 to allow matching sales ProductIDs P101–P110
        api_products_101_200 = fetch_products_101_to_200()
        mapping_101_200 = create_product_mapping(api_products_101_200)
        enriched_101_200 = enrich_sales_data(valid_records, mapping_101_200)

        enriched_success = sum(1 for t in enriched_101_200 if t.get("API_Match") is True)
        success_rate = (enriched_success / len(enriched_101_200) * 100) if enriched_101_200 else 0.0
        print(f"✓ Enriched {enriched_success}/{len(enriched_101_200)} transactions ({success_rate:.1f}%)")
        print("")

        # [8/10] Saving enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(
            enriched_100,
            filename=r"data\enriched_sales_data_limit_100.txt",
            comment="Task 3.1a output: limit=100 (IDs 1–100). Sales ProductIDs P101–P110 likely won't match."
        )
        save_enriched_data(
            enriched_101_200,
            filename=r"data\enriched_sales_data_101_200.txt",
            comment="Supplemental enrichment output using IDs 101–200 for sales ProductIDs."
        )
        print("✓ Saved to: data\\enriched_sales_data_limit_100.txt")
        print("✓ Saved to: data\\enriched_sales_data_101_200.txt")
        print("")

        # [9/10] Generating comprehensive report (Task 4.1)
        print("[9/10] Generating report...")
        generate_sales_report(
            valid_records,
            enriched_101_200,
            output_file=r"output\sales_report.txt",
        )
        print("✓ Report saved to: output\\sales_report.txt")
        print("")

        # [10/10] Complete
        print("[10/10] Process Complete!")
        print("=" * 40)
        print("Files generated:")
        print(" - output\\analysis_report.txt")
        print(" - output\\sales_report.txt")
        print(" - data\\enriched_sales_data_limit_100.txt")
        print(" - data\\enriched_sales_data_101_200.txt")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR: Something went wrong, but the program did not crash.")
        print("Details:", str(e))


if __name__ == "__main__":
    main()
