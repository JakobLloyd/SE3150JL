"""Checkout depends on remote tax service."""

# Checkout requirements:
#
# - Calculate the subtotal from each item's
#   price and quantity.
#
# - Request the current tax rate from the
#   external tax service.
#
# - Use the customer's postal code to select
#   the correct tax jurisdiction.
#
# - Display the jurisdiction used.
#
# - Add the calculated tax to the subtotal.
#
# - Return the final total rounded
#   to two decimal places.
#
# It is critical that checkout succeeds.
# A failure prevents the customer from
# completing the purchase and directly
# affects company revenue.

class TaxServiceClient:
    def __init__(self, available=True):
        self.available = available

    def rate_for(self, postal_code):
        if not self.available:
            raise ConnectionError("Tax service did not respond")
        return {"rate": 0.0725, "jurisdiction": "Washington County"}


class Checkout:
    def __init__(self, tax_client):
        self.tax_client = tax_client

    def total(self, items, postal_code):
        subtotal = sum(item["price"] * item["quantity"] for item in items)
        response = self.tax_client.rate_for(postal_code)
        tax = subtotal * response["rate"]
        print(f"Tax jurisdiction: {response['jurisdiction']}")
        return round(subtotal + tax, 2)


if __name__ == "__main__":
    checkout = Checkout(TaxServiceClient(available=False))
    print(checkout.total([{"price": 29.95, "quantity": 2}], "84770"))

