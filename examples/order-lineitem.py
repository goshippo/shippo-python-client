from datetime import datetime

import shippo

"""
In this example, we are creating (and consuming) an order object with lineitem(s).
"""

# Replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"

# Example address_from object dict
# The complete reference for the address object is available here: https://goshippo.com/docs/reference#addresses
address_from = {
    "name": "Shippo Team",
    "street1": "965 Mission St",
    "street2": "Unit 480",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94103",
    "country": "US",
    "phone": "+1 555 341 9393",
}

# Example address_to object dict
# The complete reference for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "name": "Shippo Friend",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}

unit_price = 2.34
unit_weight = 25.45
unit_quantity = 2
line_item1 = {
        "title": "Demo Line Item Object",
        "sku": "demo_1234",
        "quantity": unit_quantity,
        "total_price": f"{unit_price:.2f}",
        "currency": "USD",
        "weight": f"{unit_weight:.2f}",
        "weight_unit": "lb",
        "manufacture_country": "US"
    }
line_items = [line_item1]

shipping_cost = 1.23
subtotal_cost = unit_price
tax_cost = 1.065*subtotal_cost
total_cost = shipping_cost + subtotal_cost + tax_cost
my_order = {
        "order_number": f"#{datetime.now().date()}",
        "order_status": "PAID",
        "to_address": address_to,
        "from_address": address_from,
        "line_items": line_items,
        "placed_at": datetime.now().isoformat(),
        "weight": f"{10.0:.2f}",
        "weight_unit": "lb",
        "shipping_method": "ground",
        "shipping_cost": f"{shipping_cost:.2f}",
        "shipping_cost_currency": "USD",
        "subtotal_price": f"{subtotal_cost:.2f}",
        "total_price": f"{total_cost:.2f}",
        "total_tax": f"{tax_cost:.2f}",
        "currency": "USD"
    }

order = shippo.Order.create(order_number=123,
                            order_status="PAID",
                            to_address=address_to,
                            from_address=address_from,
                            line_items=[line_item1],
                            placed_at=datetime.now().isoformat(),
                            weight=unit_weight*unit_quantity,
                            weight_unit="lb")
print(order)
