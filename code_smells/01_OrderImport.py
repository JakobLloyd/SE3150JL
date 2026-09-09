"""This function imports orders from a .csv"""

import csv
from datetime import datetime


def import_orders(csv_text):
    rows = list(csv.DictReader(csv_text.splitlines()))
    accepted = []
    rejected = []
    warnings = []
    totals_by_region = {}
    totals_by_category = {}
    totals_by_rep = {}
    payment_counts = {}
    status_counts = {}
    grand_subtotal = 0.0
    grand_tax = 0.0
    grand_shipping = 0.0
    grand_total = 0.0

    # Normalize customer id
    for row in rows:
        row["customer_id"] = row.get("customer_id", "").strip()

    # Normalize first name
    for row in rows:
        row["first_name"] = row.get("first_name", "").strip().title()

    # Normalize last name
    for row in rows:
        row["last_name"] = row.get("last_name", "").strip().title()

    # Normalize email
    for row in rows:
        row["email"] = row.get("email", "").strip().lower()

    # Normalize phone
    for row in rows:
        row["phone"] = row.get("phone", "").strip()

    # Normalize street
    for row in rows:
        row["street"] = row.get("street", "").strip().title()

    # Normalize city
    for row in rows:
        row["city"] = row.get("city", "").strip().title()

    # Normalize state
    for row in rows:
        row["state"] = row.get("state", "").strip().upper()

    # Normalize postal code
    for row in rows:
        row["postal_code"] = row.get("postal_code", "").strip()

    # Normalize country
    for row in rows:
        row["country"] = row.get("country", "").strip().upper()

    # Normalize product code
    for row in rows:
        row["product_code"] = row.get("product_code", "").strip().upper()

    # Normalize product name
    for row in rows:
        row["product_name"] = row.get("product_name", "").strip().title()

    # Normalize category
    for row in rows:
        row["category"] = row.get("category", "").strip().title()

    # Normalize sales rep
    for row in rows:
        row["sales_rep"] = row.get("sales_rep", "").strip().title()

    # Normalize sales region
    for row in rows:
        row["sales_region"] = row.get("sales_region", "").strip().upper()

    # Normalize order status
    for row in rows:
        row["order_status"] = row.get("order_status", "").strip().lower()

    # Normalize payment method
    for row in rows:
        row["payment_method"] = row.get("payment_method", "").strip().lower()

    # Normalize coupon code
    for row in rows:
        row["coupon_code"] = row.get("coupon_code", "").strip().upper()

    # Normalize shipping method
    for row in rows:
        row["shipping_method"] = row.get("shipping_method", "").strip().lower()

    # Normalize tracking number
    for row in rows:
        row["tracking_number"] = row.get("tracking_number", "").strip().upper()

    # Parse quantity
    for row in rows:
        try:
            row["quantity"] = int(row.get("quantity", 0))
        except (TypeError, ValueError):
            row["quantity"] = int(0)
            row.setdefault("errors", []).append("invalid quantity")

    # Parse unit price
    for row in rows:
        try:
            row["unit_price"] = float(row.get("unit_price", 0))
        except (TypeError, ValueError):
            row["unit_price"] = float(0)
            row.setdefault("errors", []).append("invalid unit_price")

    # Parse discount percent
    for row in rows:
        try:
            row["discount_percent"] = float(row.get("discount_percent", 0))
        except (TypeError, ValueError):
            row["discount_percent"] = float(0)
            row.setdefault("errors", []).append("invalid discount_percent")

    # Parse tax rate
    for row in rows:
        try:
            row["tax_rate"] = float(row.get("tax_rate", 0))
        except (TypeError, ValueError):
            row["tax_rate"] = float(0)
            row.setdefault("errors", []).append("invalid tax_rate")

    # Parse shipping cost
    for row in rows:
        try:
            row["shipping_cost"] = float(row.get("shipping_cost", 0))
        except (TypeError, ValueError):
            row["shipping_cost"] = float(0)
            row.setdefault("errors", []).append("invalid shipping_cost")

    # Parse dates
    for row in rows:
        try:
            row["order_date"] = datetime.strptime(row.get("order_date", ""), "%Y-%m-%d").date()
        except ValueError:
            row["order_date"] = None
            row.setdefault("errors", []).append("invalid order date")
        try:
            row["ship_date"] = datetime.strptime(row.get("ship_date", ""), "%Y-%m-%d").date()
        except ValueError:
            row["ship_date"] = None


    # Validate records
    for row in rows:
        row.setdefault("errors", [])
        if not row["customer_id"]:
            row["errors"].append("missing customer id")
        if not row["first_name"]:
            row["errors"].append("missing first name")
        if not row["last_name"]:
            row["errors"].append("missing last name")
        if "@" not in row["email"]:
            row["errors"].append("invalid email")
        if row["quantity"] <= 0:
            row["errors"].append("quantity must be positive")
        if row["unit_price"] < 0:
            row["errors"].append("price cannot be negative")
        if not 0 <= row["discount_percent"] <= 100:
            row["errors"].append("invalid discount")
        if not 0 <= row["tax_rate"] <= 0.25:
            row["errors"].append("invalid tax rate")
        if not row["product_code"]:
            row["errors"].append("missing product code")
        if row["country"] == "US" and len(row["state"]) != 2:
            row["errors"].append("invalid US state")
        if row["order_status"] not in {"new", "paid", "shipped", "cancelled", "refunded"}:
            row["errors"].append("invalid status")
        if row["payment_method"] not in {"card", "cash", "invoice", "transfer"}:
            row["errors"].append("invalid payment method")
        if row["ship_date"] and row["order_date"] and row["ship_date"] < row["order_date"]:
            row["errors"].append("ship date precedes order date")
        if row["order_status"] == "shipped" and not row["tracking_number"]:
            row["errors"].append("shipped order lacks tracking")

    # Calculate each order
    for row in rows:
        subtotal = row["quantity"] * row["unit_price"]
        discount = subtotal * row["discount_percent"] / 100
        taxable = subtotal - discount
        tax = taxable * row["tax_rate"]
        shipping = row["shipping_cost"]
        if row["shipping_method"] == "pickup":
            shipping = 0
        if taxable >= 100 and row["shipping_method"] == "ground":
            shipping = 0
        total = taxable + tax + shipping
        row["subtotal"] = round(subtotal, 2)
        row["discount"] = round(discount, 2)
        row["tax"] = round(tax, 2)
        row["shipping"] = round(shipping, 2)
        row["total"] = round(total, 2)

    # Separate accepted and rejected records
    for row in rows:
        if row["errors"]:
            rejected.append(row)
        else:
            accepted.append(row)

    # Build summaries
    for row in accepted:
        region = row["sales_region"] or "UNASSIGNED"
        category = row["category"] or "UNCATEGORIZED"
        rep = row["sales_rep"] or "UNASSIGNED"
        totals_by_region[region] = totals_by_region.get(region, 0) + row["total"]
        totals_by_category[category] = totals_by_category.get(category, 0) + row["total"]
        totals_by_rep[rep] = totals_by_rep.get(rep, 0) + row["total"]
        payment_counts[row["payment_method"]] = payment_counts.get(row["payment_method"], 0) + 1
        status_counts[row["order_status"]] = status_counts.get(row["order_status"], 0) + 1
        grand_subtotal += row["subtotal"]
        grand_tax += row["tax"]
        grand_shipping += row["shipping"]
        grand_total += row["total"]

    # Detect noteworthy records
    for row in accepted:
        if row["discount_percent"] >= 40:
            warnings.append(f'Large discount: {row["product_code"]}')
        if row["total"] >= 5000:
            warnings.append(f'Large order: {row["customer_id"]}')
        if row["sales_rep"] == "":
            warnings.append(f'No sales rep: {row["customer_id"]}')
        if row["order_status"] == "paid" and row["order_date"] and (datetime.now().date() - row["order_date"]).days > 14:
            warnings.append(f'Possible shipping delay: {row["customer_id"]}')

    # Sort output
    accepted.sort(key=lambda row: (-row["total"], row["customer_id"]))
    rejected.sort(key=lambda row: row["customer_id"])
    warnings.sort()

    # Format a printable report
    report = []
    report.append("ORDER IMPORT REPORT")
    report.append("=" * 60)
    report.append(f"Rows received: {len(rows)}")
    report.append(f"Rows accepted: {len(accepted)}")
    report.append(f"Rows rejected: {len(rejected)}")
    report.append("")
    report.append("FINANCIAL TOTALS")
    report.append(f"Subtotal: ${grand_subtotal:,.2f}")
    report.append(f"Tax: ${grand_tax:,.2f}")
    report.append(f"Shipping: ${grand_shipping:,.2f}")
    report.append(f"Total: ${grand_total:,.2f}")
    report.append("")
    report.append("TOTALS BY REGION")
    for name, amount in sorted(totals_by_region.items()):
        report.append(f"{name}: ${amount:,.2f}")
    report.append("")
    report.append("TOTALS BY CATEGORY")
    for name, amount in sorted(totals_by_category.items()):
        report.append(f"{name}: ${amount:,.2f}")
    report.append("")
    report.append("TOTALS BY SALES REP")
    for name, amount in sorted(totals_by_rep.items()):
        report.append(f"{name}: ${amount:,.2f}")
    report.append("")
    report.append("WARNINGS")
    if warnings:
        for warning in warnings:
            report.append(f"- {warning}")
    else:
        report.append("None")
    report.append("")
    report.append("REJECTED ROWS")
    for row in rejected:
        report.append(f'{row["customer_id"] or "(unknown)"}: {'; '.join(row["errors"])}')

    report.append("")
    report.append("PAYMENT METHODS")
    for name, count in sorted(payment_counts.items()):
        report.append(f"{name}: {count}")
    report.append("")
    report.append("ORDER STATUS")
    for name, count in sorted(status_counts.items()):
        report.append(f"{name}: {count}")
    report.append("")
    report.append("LARGEST ACCEPTED ORDERS")
    for row in accepted[:5]:
        report.append(
            f'{row["customer_id"]}: {row["product_name"] or row["product_code"]} '
            f'${row["total"]:,.2f}'
        )
    report.append("")
    report.append("IMPORT COMPLETE")
    report.append(f"Review required: {'yes' if rejected or warnings else 'no'}")

    return {
        "accepted": accepted,
        "rejected": rejected,
        "warnings": warnings,
        "totals_by_region": totals_by_region,
        "totals_by_category": totals_by_category,
        "totals_by_rep": totals_by_rep,
        "payment_counts": payment_counts,
        "status_counts": status_counts,
        "report": "\n".join(report),
    }


if __name__ == "__main__":
    sample = """customer_id,first_name,last_name,email,quantity,unit_price,discount_percent,tax_rate,shipping_cost,product_code,order_status,payment_method,order_date,ship_date,country,state
C-1,Jamie,Ng,jamie@example.com,2,49.95,10,0.0725,8.00,P-10,paid,card,2026-09-01,,US,UT"""
    print(import_orders(sample)["report"])



'''
1. The code is repetitve and could have generalized functions for stripping rather than repeating the same operations.
2. The code is way too long and could be broken down into smaller functions for better readability and maintainability.








'''