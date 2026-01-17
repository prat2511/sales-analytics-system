from __future__ import annotations
from pathlib import Path
from typing import List, Tuple,Dict, Any

def read_sales_data(filename: str | Path) -> list[str]:
    """
	Q2 Task 1.&
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    path = Path(filename)

    if not path.exists():
        print(f"ERROR: File not found -> {path}")
        return []

    for enc in encodings:
        try:
            with open(path, encoding=enc) as file:
                lines = file.readlines()

            # Remove empty lines and skip header
            cleaned = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    cleaned.append(line)

            return cleaned

        except UnicodeDecodeError:
            continue

    print("ERROR: Unable to read file with supported encodings.")
    return []





def _parse_line(line: str) -> Dict[str, Any] | None:
    """
    Expected pipe-delimited format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
    Cleans:
    - commas in ProductName
    - commas in numeric fields (1,500 -> 1500)
    """
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) != 8:
        return None

    transaction_id, date_s, product_id, product_name, qty_s, price_s, customer_id, region = parts

    # Clean product name: remove commas
    product_name = product_name.replace(",", "").strip()

    # Clean numeric strings: remove commas
    qty_s = qty_s.replace(",", "").strip()
    price_s = price_s.replace(",", "").strip()

    # Convert types
    try:
        quantity = int(qty_s)
        unit_price = float(price_s)
    except ValueError:
        return None

    # Return dictionary 
    return {
        "transaction_id": transaction_id,
        "date": date_s,
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "unit_price": unit_price,
        "customer_id": customer_id,
        "region": region,
    }



def load_sales_data(file_path: str | Path) -> Tuple[List[SalesRecord], int, int]:
    """
    Loads and validates sales data from a text file.

    Returns: Q1
        valid_records,
        total_records_parsed,
        invalid_records_removed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = read_sales_data(path)

    total_parsed = len(lines)
    valid: List[Dict[str, Any]] = []
    invalid = 0

    for ln in lines:
        rec = _parse_line(ln)
        if rec is None:
            invalid += 1
        else:
            valid.append(rec)

    return valid, total_parsed, invalid


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Returns: (valid_transactions, invalid_count, filter_summary)
    """
    total_input = len(transactions)
    invalid = 0
    valid = []

    # Collect region options + amount range from valid candidates
    regions_set = set()
    amounts = []

    # --------- Validation ----------
    for t in transactions:
        # Required fields
        required_keys = ["transaction_id", "product_id", "customer_id", "region", "quantity", "unit_price"]
        if any(k not in t or t[k] in (None, "") for k in required_keys):
            invalid += 1
            continue

        # ID format validation
        if not str(t["transaction_id"]).startswith("T"):
            invalid += 1
            continue
        if not str(t["product_id"]).startswith("P"):
            invalid += 1
            continue
        if not str(t["customer_id"]).startswith("C"):
            invalid += 1
            continue

        # Quantity and UnitPrice validation
        try:
            qty = int(t["quantity"])
            price = float(t["unit_price"])
        except (ValueError, TypeError):
            invalid += 1
            continue

        if qty <= 0 or price <= 0:
            invalid += 1
            continue

        # Compute amount
        amount = qty * price
        t["amount"] = amount  # store amount for filtering/reporting

        valid.append(t)
        regions_set.add(t["region"])
        amounts.append(amount)

    # Print available options
    available_regions = sorted(regions_set)
    print("\n=== Filter Info ===")
    print(f"Available regions: {available_regions}")

    if amounts:
        print(f"Transaction amount range: min={min(amounts):.2f}, max={max(amounts):.2f}")
    else:
        print("Transaction amount range: min=0.00, max=0.00")

    # --------- Filtering ----------
    filtered_by_region = 0
    filtered_by_amount = 0

    filtered = valid

    # Region filter
    if region is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["region"] == region]
        filtered_by_region = before - len(filtered)
        print(f"After region filter ({region}): {len(filtered)} records")

    # Amount filters
    if min_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["amount"] >= float(min_amount)]
        filtered_by_amount += before - len(filtered)
        print(f"After min_amount filter ({min_amount}): {len(filtered)} records")

    if max_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["amount"] <= float(max_amount)]
        filtered_by_amount += before - len(filtered)
        print(f"After max_amount filter ({max_amount}): {len(filtered)} records")

    summary = {
        "total_input": total_input,
        "invalid": invalid,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered),
    }

    return filtered, invalid, summary
