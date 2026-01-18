import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    TASK 3.1a (MANDATORY – DO NOT CHANGE)

    Fetches first 100 products only.
    NOTE:
    DummyJSON returns products with IDs 1–100 here.
    Sales ProductIDs are P101–P110, so mapping WILL FAIL.
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API fetch (limit=100): fetched products with IDs 1–100")
        return data.get("products", [])
    except Exception as e:
        print("API fetch failed (limit=100):", e)
        return []


def fetch_products_101_to_200():
    """
    SUPPORT FUNCTION (DATA COMPATIBILITY FIX)

    Sales data ProductIDs range from P101–P110.
    DummyJSON supports product IDs up to ~194.

    This function fetches products with IDs 101–200
    using single-product API calls.
    """
    products = []

    for pid in range(101, 201):
        try:
            r = requests.get(f"{BASE_URL}/{pid}", timeout=5)
            if r.status_code == 200:
                products.append(r.json())
        except Exception:
            continue

    print("API fetch (101–200): fetched products matching sales ProductIDs")
    return products


def create_product_mapping(api_products):
    mapping = {}
    for p in api_products:
        mapping[p["id"]] = {
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating"),
        }
    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.

    NOTE:
      product_id, product_name, unit_price, customer_id, region, etc.
    """
    enriched = []

    for t in transactions:
        row = dict(t)

        product_id = row.get("product_id", "")
        try:
            numeric_id = int(str(product_id).replace("P", ""))
        except Exception:
            numeric_id = None

        api_data = product_mapping.get(numeric_id) if numeric_id is not None else None

        if api_data:
            row["API_Category"] = api_data.get("category")
            row["API_Brand"] = api_data.get("brand")
            row["API_Rating"] = api_data.get("rating")
            row["API_Match"] = True
        else:
            row["API_Category"] = None
            row["API_Brand"] = None
            row["API_Rating"] = None
            row["API_Match"] = False

        enriched.append(row)

    return enriched



def save_enriched_data(enriched_transactions, filename, comment):
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]
    def v(x):
	    return "" if x is None else str(x)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {comment}\n")
        f.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                v(t.get("transaction_id")),
                v(t.get("date")),
                v(t.get("product_id")),
                v(t.get("product_name")),
                v(t.get("quantity")),
                v(t.get("unit_price")),
                v(t.get("customer_id")),
                v(t.get("region")),
                v(t.get("API_Category")),
                v(t.get("API_Brand")),
                v(t.get("API_Rating")),
                v(t.get("API_Match")),
            ]
            f.write("|".join(row) + "\n")

