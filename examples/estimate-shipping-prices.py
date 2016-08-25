import shippo

"""
In this tutorial we want to calculate our average shipping costs so 
we set pricing for customers.

We have a sender address, a parcel and a set of delivery zip codes.
We will retrieve all available shipping rates for each delivery
address and calculate the min, max and average price for specific
transit time windows (next day, 3 days, 7 days).

Sample output:
For a delivery window of 1 days:
--> Min. costs: 5.81
--> Max. costs: 106.85
--> Avg. costs: 46.91


For a delivery window of 3 days:
--> Min. costs: 5.81
--> Max. costs: 106.85
--> Avg. costs: 34.99


For a delivery window of 7 days:
--> Min. costs: 3.22
--> Max. costs: 106.85
--> Avg. costs: 29.95

"""

# Define delivery windows in max. days
# Pick an east coast, a west coast and a mid-west destination
DELIVERY_WINDOWS = [1, 3, 7]
DESTINATION_ADDRESSES_ZIP_CODES = [10007, 60290, 95122]

# replace <API-KEY> with your key
shippo.api_key = "<API-KEY>"

# sample address_from
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses
address_from = {
    "object_purpose": "QUOTE",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94117",
    "country": "US"
}

# sample address_to placeholder object
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "object_purpose": "QUOTE",
    "country": "US"
}

# Sample parcel, make sure to replace placeholders with your average shipment size 
# The complete reference for parcel object is here: https://goshippo.com/docs/reference#parcels

parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb",
}

"""
For each destination address we now create a Shipment object
and store the min, max, average shipping rates per delivery window.
"""
shipping_costs = {}

for delivery_address_zip_code in DESTINATION_ADDRESSES_ZIP_CODES:
    # Change delivery address to current delivery address
    address_to['zip'] = delivery_address_zip_code
    # Creating the shipment object. async=False indicates that the function will wait until all
    # rates are generated before it returns.
    # The reference for the shipment object is here: https://goshippo.com/docs/reference#shipments
    # By default Shippo API operates on an async basis. You can read about our async flow here: https://goshippo.com/docs/async
    
    shipment = shippo.Shipment.create(
        object_purpose='QUOTE',
        address_from=address_from,
        address_to=address_to,
        parcel=parcel,
        async=False
    )
    # Rates are stored in the `rates_list` array
    # The details on the returned object are here: https://goshippo.com/docs/reference#rates
    
    rates = shipment.rates_list
    print "Returned %s rates to %s" % (len(rates), delivery_address_zip_code)
    # We now store the shipping cost for each delivery window in our
    # `shipping_costs` dictionary to analyse it later.
    for delivery_window in DELIVERY_WINDOWS:
        # Filter rates that are within delivery window
        eligible_rates = (rate for rate in rates if rate['days'] <= delivery_window)
        new_rate_prices = list(float(rate['amount']) for rate in eligible_rates if rate['amount'])
        existing_rate_prices = shipping_costs[str(delivery_window)] if str(delivery_window) in shipping_costs else []
        shipping_costs[str(delivery_window)] = existing_rate_prices + new_rate_prices

"""
Now that we have the costs per delivery window for all sample destination
addresses we can return the min, max and average values.
"""
for delivery_window in DELIVERY_WINDOWS:
    if not str(delivery_window) in shipping_costs:
        print "No rates found for delivery window of %s days" % delivery_window
    else:
        costs = shipping_costs[str(delivery_window)]
        print "For a delivery window of %s days:" % delivery_window
        print "--> Min. costs: %0.2f" % min(costs)
        print "--> Max. costs: %0.2f" % max(costs)
        print "--> Avg. costs: %0.2f" % (sum(costs) / float(len(costs)))
        print "\n"
        
# For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/