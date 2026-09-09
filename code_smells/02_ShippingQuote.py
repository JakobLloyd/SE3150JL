"""This function creates a shipping quote based on the rules."""

# Shipping rules:
#
# - Alaska and Hawaii use air shipping.
#
# - US orders over 70 pounds require freight.
#   If freight is unavailable, reject the order.
#
# - US overnight orders use express shipping
#   when express service is available.
#
# - Other US orders use ground shipping.
#
# - Canada and Mexico use international ground.
#   Food shipments require three extra days.
#
# - Other countries require international service.
#
# - International battery shipments require
#   permission from the destination country.
#
# - Fragile orders cost $12 extra.
#   Fragile ground orders take one extra day.
#
# - Gold members receive 25% off,
#   except on freight shipments.
#
# - Silver members receive $5 off
#   when shipping costs more than $25.
#
# - Orders placed Friday through Sunday
#   take two additional days.
#
# Return the shipping service, final cost,
# and estimated arrival date.
from datetime import date, timedelta


def shipping_quote(order, customer, destination, carriers):
    if destination["country"] == "US":
        if destination["state"] in {"AK", "HI"}:
            service = "air"
            cost = 24.00 + order["weight"] * 1.80
            days = 5
        elif order["weight"] > 70:
            if carriers["freight_available"]:
                service = "freight"
                cost = 85.00 + order["weight"] * 0.55
                days = 6
            else:
                return None
        elif order["overnight"]:
            if carriers["express_available"]:
                service = "express"
                cost = 32.00 + order["weight"] * 2.20
                days = 1
            else:
                service = "ground"
                cost = 9.00 + order["weight"] * 0.65
                days = 4
        else:
            service = "ground"
            cost = 9.00 + order["weight"] * 0.65
            days = 4
    elif destination["country"] in {"CA", "MX"}:
        service = "international-ground"
        cost = 20.00 + order["weight"] * 1.35
        days = 8
        if order["contains_food"]:
            days += 3
    else:
        if not carriers["international_available"]:
            return None
        if order["contains_battery"]:
            if destination["allows_batteries"]:
                service = "international-special"
                cost = 48.00 + order["weight"] * 2.40
                days = 12
            else:
                return None
        else:
            service = "international-air"
            cost = 38.00 + order["weight"] * 1.90
            days = 9

    if order["fragile"]:
        cost += 12.00
        if service == "ground":
            days += 1
    if customer["membership"] == "gold":
        if service != "freight":
            cost *= 0.75
    elif customer["membership"] == "silver" and cost > 25:
        cost -= 5
    if date.today().weekday() >= 4:
        days += 2

    return {"service": service, "cost": round(cost, 2),
            "arrival": date.today() + timedelta(days=days)}


if __name__ == "__main__":
    print(shipping_quote(
        {"weight": 12, "overnight": False, "contains_food": False,
         "contains_battery": True, "fragile": True},
        {"membership": "gold"},
        {"country": "DE", "state": "", "allows_batteries": True},
        {"freight_available": True, "express_available": True,
         "international_available": True},
    ))

