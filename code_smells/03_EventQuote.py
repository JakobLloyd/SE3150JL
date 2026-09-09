"""Create a quote for an event venue."""

# Event quote rules:
#
# - Record the customer's name and email.
#
# - Record the event date, start time,
#   number of guests, and duration.
#
# - Room rental rates are hourly:
#     Cedar: $90
#     Maple: $140
#     Oak:   $210
#
# - Tables cost $8 each.
# - Chairs cost $2 each.
# - A projector costs $45.
# - Microphones cost $18 each.
#
# - Security staff cost $28 per hour
#   for each staff member.
#
# - Basic cleaning costs $60.
# - Full cleaning costs $140.
#
# - Food cost equals the number of meals
#   multiplied by the price per meal.
#
# - The COMMUNITY10 discount code
#   reduces the subtotal by 10%.
#
# - Apply tax after applying the discount.
#
# - Calculate the required deposit
#   as a percentage of the final total.
#
# Return the customer contact information,
# event details, guest count, total price,
# and required deposit.

def create_event_quote(customer_name, customer_email, event_date, start_time,
                       guest_count, duration_hours, room_name, tables,
                       chairs, meals, meal_price, projector, microphones,
                       security_staff, cleaning_level, tax_rate,
                       deposit_percent, discount_code):
    room_cost = duration_hours * {"cedar": 90, "maple": 140, "oak": 210}[room_name]
    equipment_cost = tables * 8 + chairs * 2
    equipment_cost += 45 if projector else 0
    equipment_cost += microphones * 18
    staffing_cost = security_staff * duration_hours * 28
    cleaning_cost = {"basic": 60, "full": 140}[cleaning_level]
    food_cost = meals * meal_price
    subtotal = room_cost + equipment_cost + staffing_cost + cleaning_cost + food_cost
    if discount_code == "COMMUNITY10":
        subtotal *= 0.90
    total = subtotal * (1 + tax_rate)
    return {"customer": customer_name, "email": customer_email,
            "event": f"{event_date} {start_time}", "guests": guest_count,
            "total": round(total, 2),
            "deposit": round(total * deposit_percent, 2)}


if __name__ == "__main__":
    print(create_event_quote("Northside Club", "events@example.com", "2026-11-14",
          "18:00", 80, 5, "maple", 10, 80, 70, 19.50, True, 2, 2,
          "full", 0.0725, 0.25, "COMMUNITY10"))

