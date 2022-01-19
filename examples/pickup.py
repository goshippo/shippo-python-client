import shippo
from datetime import datetime, timedelta

"""
In this tutorial we have an order with a sender address,
recipient address and parcel. The shipment is going from the
United States to an international location.

In addition to that we know that the customer expects the
shipment to arrive within 3 days. We now want to purchase
the cheapest shipping label with a transit time <= 3 days.
"""

# replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"

# Example address_from object dict
# The complete reference for the address object is available here: https://goshippo.com/docs/reference#addresses
address_from = {
    "company": "",
    "street_no": "",
    "name": "Shippo Friend",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
    "email": "support@goshippo.com"
}

# Example address_to object dict
# The complete reference for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to_international = {
    "name": "Mrs. Hippo",
    "street1": "200 University Ave W",
    "street2": "",
    "city": "Waterloo",
    "state": "ON",
    "zip": "N2L 3G1",
    "country": "CA",
    "phone": "+1 555 341 9393",
    "email": "support@goshippo.com",
    "metadata": "For Order Number 123"
}

# parcel object dict
# The complete reference for parcel object is here: https://goshippo.com/docs/reference#parcels
parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb"
}

# Example CustomsItems object.
#  The complete reference for customs object is here: https://goshippo.com/docs/reference#customsitems
customs_item = {
    "description": "T-Shirt",
    "quantity": 2,
    "net_weight": "400",
    "mass_unit": "g",
    "value_amount": "20",
    "value_currency": "USD",
    "origin_country": "US",
    "tariff_number": ""
}

# Creating the CustomsDeclaration
# The details on creating the CustomsDeclaration is here: https://goshippo.com/docs/reference#customsdeclarations
customs_declaration = shippo.CustomsDeclaration.create(
    contents_type='MERCHANDISE',
    contents_explanation='T-Shirt purchase',
    non_delivery_option='RETURN',
    certify=True,
    certify_signer='Mr Hippo',
    items=[customs_item])

# Creating the shipment object. asynchronous=False indicates that the function will wait until all
# rates are generated before it returns.

# The reference for the shipment object is here: https://goshippo.com/docs/reference#shipments
# By default Shippo API operates on an async basis. You can read about our async flow here: https://goshippo.com/docs/async
shipment_international = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to_international,
    parcels=[parcel],
    customs_declaration=customs_declaration.object_id,
    asynchronous=False)

# Get the first usps or dhl express rate.
# The details on the returned object are here: https://goshippo.com/docs/reference#rates
filtered_rates = []
for rate in shipment_international.rates:
    if rate.provider.lower() == "usps" or rate.provider.lower() == "dhl_express":
        filtered_rates.append(rate)
    # return strtolower($rate['provider']) == 'usps' Or strtolower($rate['provider']) == 'dhl_express';

rate_international = filtered_rates[0]
selected_rate_carrier_account = rate_international.carrier_account

# Purchase the desired rate.
# The complete information about purchasing the label: https://goshippo.com/docs/reference#transaction-create
transaction_international = shippo.Transaction.create(
    rate=rate_international.object_id, asynchronous=False)

if transaction_international.status != "SUCCESS":
    print("Failed purchasing the label due to:")
    for message in transaction_international.messages:
        print("- %s" % message['text'])

# $pickupTimeStart = date('Y-m-d H:i:s', time());
# $pickupTimeEnd = date('Y-m-d H:i:s', time() + 60*60*24);
pickupTimeStart = datetime.now() + timedelta(hours=1)
pickupTimeEnd = pickupTimeStart + timedelta(days=1)

# Schedule the pickup
# Only 1 pickup can be scheduled in a day
try:
    pickup = shippo.Pickup.create(
        carrier_account= selected_rate_carrier_account,
        location= {
            "building_location_type" : "Knock on Door",
            "address" : address_from,
        },
        transactions= [transaction_international.object_id],
        requested_start_time= pickupTimeStart.isoformat() + "Z",
        requested_end_time= pickupTimeEnd.isoformat() + "Z",
        is_test= False
    )
except shippo.error.InvalidRequestError as err:
    print("A pickup has already been scheduled for today.")
else:
    if pickup.status == "SUCCESS":
        print("Pickup has been scheduled")
    else:
        print("Failed scheduling a pickup:")
        for message in pickup.messages:
            print("- %s" % message['text'])

# For more tutorials of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
