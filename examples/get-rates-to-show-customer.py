import shippo

"""
In this tutorial we have an order with a sender address,
recipient address and parcel. We will retrieve all avail-
able shipping rates, display them to the user and purchase
a label after the user has selected a rate.
"""

# for demo purposes we set the max. transit time here
MAX_TRANSIT_TIME_DAYS = 3

# replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"

# Example address_from object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses
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
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "name": "Shippo Friend",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}

# parcel object dict
# The complete reference for parcel object is here: https://goshippo.com/docs/reference#parcels
parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb",
}

# Example shipment object
# For complete reference to the shipment object: https://goshippo.com/docs/reference#shipments
# This object has asynchronous=False, indicating that the function will wait until all rates are generated before it returns.
# By default, Shippo handles responses asynchronously. However this will be depreciated soon. Learn more: https://goshippo.com/docs/async
shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=[parcel],
    asynchronous=False
)

# Rates are stored in the `rates` array
# The details on the returned object are here: https://goshippo.com/docs/reference#rates
rates = shipment.rates

"""
You can now show those rates to the user in your UI.
Most likely you want to show some of the following fields:
- provider (carrier name)
- servicelevel_name
- amount (price of label - you could add e.g. a 10% markup here)
- days (transit time)
Don't forget to store the `object_id` of each Rate so that you
can use it for the label purchase later.
"""

# After the user has selected a rate, use the corresponding object_id
selected_rate_object_id = '<SELECTED-RATE-OBJECT-ID>'

# Purchase the desired rate. asynchronous=False indicates that the function will wait until the
# carrier returns a shipping label before it returns
transaction = shippo.Transaction.create(
    rate=selected_rate_object_id, asynchronous=False)

# print the shipping label from label_url
# Get the tracking number from tracking_number
if transaction.status == "SUCCESS":
    print("Purchased label with tracking number %s" %
          transaction.tracking_number)
    print("The label can be downloaded at %s" % transaction.label_url)
else:
    print("Failed purchasing the label due to:")
    for message in transaction.messages:
        print("- %s" % message['text'])

# For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
