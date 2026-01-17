from typing import List, Dict


def compute_revenue_per_category(transactions: List[Dict]) -> Dict[str, float]:
    revenue = {}

    for t in transactions:
        category = t["product_id"]
        amount = t["quantity"] * t["unit_price"]

        revenue[category] = revenue.get(category, 0) + amount

    return revenue


def top_selling_product(transactions: List[Dict]):
    product_qty = {}

    for t in transactions:
        product = t["product_name"]
        product_qty[product] = product_qty.get(product, 0) + t["quantity"]

    top_product = max(product_qty, key=product_qty.get)
    return top_product, product_qty[top_product]


def sales_distribution_by_region(transactions: List[Dict]) -> Dict[str, float]:
    region_revenue = {}
    total_revenue = 0

    for t in transactions:
        amount = t["quantity"] * t["unit_price"]
        region = t["region"]

        region_revenue[region] = region_revenue.get(region, 0) + amount
        total_revenue += amount

    # Convert to percentage
    distribution = {}
    for region, rev in region_revenue.items():
        distribution[region] = (rev / total_revenue) * 100 if total_revenue else 0

    return distribution

# Task 3 2.1 a.
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    Sum of (Quantity * UnitPrice) across all transactions
    """
    total = 0.0

    for t in transactions:
        total += t["quantity"] * t["unit_price"]

    return total
# Task 3 2.1 b.
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns:
    Dictionary with total sales, transaction count,
    and percentage contribution per region.
    """
    region_data = {}
    overall_sales = 0.0

    # Step 1: Aggregate totals per region
    for t in transactions:
        region = t["region"]
        amount = t["quantity"] * t["unit_price"]

        overall_sales += amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Step 2: Calculate percentage contribution
    for region in region_data:
        region_total = region_data[region]["total_sales"]
        percentage = (region_total / overall_sales) * 100 if overall_sales > 0 else 0
        region_data[region]["percentage"] = round(percentage, 2)

    # Step 3: Sort by total_sales descending
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data

# Task 3 2.1 c.
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}

    # Step 1: aggregate by product_name
    for t in transactions:
        name = t["product_name"]
        qty = t["quantity"]
        amount = t["quantity"] * t["unit_price"]

        if name not in product_stats:
            product_stats[name] = {"total_qty": 0, "total_revenue": 0.0}

        product_stats[name]["total_qty"] += qty
        product_stats[name]["total_revenue"] += amount

    # Step 2: convert to list of tuples
    result = []
    for name, stats in product_stats.items():
        result.append((name, stats["total_qty"], round(stats["total_revenue"], 2)))

    # Step 3: sort by total quantity sold (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    # Step 4: return top n
    return result[:n]

# Task 3 2.1 d.
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """
    customers = {}

    # Step 1: aggregate by customer_id
    for t in transactions:
        cid = t["customer_id"]
        product = t["product_name"]
        amount = t["quantity"] * t["unit_price"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(product)

    # Step 2: compute average order value & convert set → list
    for cid, data in customers.items():
        data["avg_order_value"] = round(
            data["total_spent"] / data["purchase_count"], 2
        )
        data["products_bought"] = list(data["products_bought"])
        data["total_spent"] = round(data["total_spent"], 2)

    # Step 3: sort customers by total_spent descending
    sorted_customers = dict(
        sorted(
            customers.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers

# Task 3 2.2 a.
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date (chronologically)

    Output:
    {
        '2024-12-01': {'revenue': ..., 'transaction_count': ..., 'unique_customers': ...},
        ...
    }
    """
    daily = {}

    for t in transactions:
        date = t["date"]
        amount = t["quantity"] * t["unit_price"]
        customer = t["customer_id"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers_set": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["unique_customers_set"].add(customer)

    # Convert set -> count and round revenue
    final = {}
    for date, data in daily.items():
        final[date] = {
            "revenue": round(data["revenue"], 2),
            "transaction_count": data["transaction_count"],
            "unique_customers": len(data["unique_customers_set"])
        }

    # Sort by date (ISO format strings sort correctly)
    final_sorted = dict(sorted(final.items(), key=lambda x: x[0]))
    return final_sorted

# Task 3 2.2 b.
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """
    trend = daily_sales_trend(transactions)

    if not trend:
        return ("", 0.0, 0)

    peak_date = max(trend.items(), key=lambda x: x[1]["revenue"])[0]
    return (peak_date, trend[peak_date]["revenue"], trend[peak_date]["transaction_count"])

# Task 3 2.3 a.
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples sorted by TotalQuantity ascending
    (ProductName, TotalQuantity, TotalRevenue)
    """
    stats = {}

    for t in transactions:
        name = t["product_name"]
        qty = t["quantity"]
        amount = t["quantity"] * t["unit_price"]

        if name not in stats:
            stats[name] = {"qty": 0, "revenue": 0.0}

        stats[name]["qty"] += qty
        stats[name]["revenue"] += amount

    low = []
    for name, s in stats.items():
        if s["qty"] < threshold:
            low.append((name, s["qty"], round(s["revenue"], 2)))

    # Sort by quantity ascending
    low.sort(key=lambda x: x[1])
    return low
