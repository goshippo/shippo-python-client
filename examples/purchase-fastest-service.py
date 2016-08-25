import shippo

"""
In this tutorial we have an order with a sender address,
recipient address and parcel information that we need to ship.

We want to get the parcel to the customer as soon as possible, 
with a max delivery time of 3 days.
"""

# for demo purposes we set the max. transit time here
MAX_TRANSIT_TIME_DAYS = 3

# Replace <API-KEY> with your key
shippo.api_key = "<API-KEY>"

# Example address_from object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses
address_from = {
    "object_purpose": "PURCHASE",
    "name": "Shippo Team",
    "street1": "965 Mission St",
    "street2": "Unit 480",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94103",
    "country": "US",
    "phone": "+1 555 341 9393",
    "email": "support@goshippo.com"
}

# Example address_to object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "object_purpose": "PURCHASE",
    "name": "Shippo Friend",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
    "email": "support@goshippo.com"
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

# Creating the shipment object. async=False indicates that the function will wait until all
# rates are generated before it returns.
# The reference for the shipment object is here: https://goshippo.com/docs/reference#shipments
# By default Shippo API operates on an async basis. You can read about our async flow here: https://goshippo.com/docs/async
shipment = shippo.Shipment.create(
    object_purpose='PURCHASE',
    address_from=address_from,
    address_to=address_to,
    parcel=parcel,
    async=False
)

# Rates are stored in the `rates_list` array
# The details on the returned object are here: https://goshippo.com/docs/reference#rates
rates = shipment.rates_list

# Find the fastest possible transite time
key = lambda x: float(x['days'])
rate = min(eligible_rate, key=lambda x: float(x['amount']))
print "Picked service %s %s for %s %s with est. transit time of %s days" % \
    (rate['provider'], rate['servicelevel_name'], rate['currency'], rate['amount'], rate['days'])

# Purchase the desired rate. async=False indicates that the function will wait until the
# carrier returns a shipping label before it returns
transaction = shippo.Transaction.create(rate=rate.object_id, async=False)

# print label_url and tracking_number
if transaction.object_status == "SUCCESS":
    print "Purchased label with tracking number %s" % transaction.tracking_number
    print "The label can be downloaded at %s" % transaction.label_url
else:
    print "Failed purchasing the label due to:"
    for message in transaction.messages:
        print "- %s" % message['text']
        
#For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
#complete documentation: https://goshippo.com/docs/