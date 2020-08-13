import shippo
import time

"""
In this example we have a shipment with multiple parcels,
note that not all carriers offer this (most notably USPS).
To ensure that this works as expected try using UPS or FedEx.
Make sure you specify a carrier_account below which is active
and allows for multi-parcel shipments!
"""

# Replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"
# replace <carrier_account> with carrier object_id
carrier_account = "<carrier_account>"

# Example address_from object dict
# The complete reference for the address object is available here:
#       https://goshippo.com/docs/reference#addresses
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
# The complete fence for the address object is available here:
#       https://goshippo.com/docs/reference#addresses

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
# The complete reference for parcel object is here:
#       https://goshippo.com/docs/reference#parcels
parcel = {
    "length": "3",
    "width": "3",
    "height": "3",
    "distance_unit": "in",
    "weight": "1",
    "mass_unit": "lb",
}

# Parcels do not need to be the same!
parcel_list = []
for parcel_piece in range(0,10):
    parcel_list.append(parcel)

print("We now have {} in this shipment!".format(len(parcel_list)))
carrier = [carrier_account]

# Example shipment object
# For complete reference to the shipment object:
#      https://goshippo.com/docs/reference#shipments
shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=parcel_list,
    carrier_accounts=carrier,
    asynchronous=True
)

# Rates are stored in the `rates` array
# The details on the returned object are here:
#      https://goshippo.com/docs/reference#rates
# For demo purposes enter the corresponding enumerated rate and press Enter.
shipment_id = shipment.object_id
print(f"the shipment_id {shipment_id}")
rates = shippo.Shipment.get_rates(shipment.object_id)
print(rates.results)
for x,y in enumerate(rates.results):
    print(f"{x}: amount: {y['amount']},rate_object_id {y['object_id']}")
the_rate = int(input("Enter number next to rate"))
rate = rates.results[the_rate]
print("rate selected: \n\n {}".format(rate))

# Purchase the desired rate with a transaction request
transaction = shippo.Transaction.create(
    rate=rate.object_id, label_file_type="PDF_A4",
    asynchronous=True)

# print the shipping label from label_url
# Get the tracking number from tracking_number
if transaction.status == "QUEUED":
    print("the_return_response async {}".format(transaction))
    #print("Purchased label with tracking number %s" %
    #      transaction.tracking_number)
    #print("The FIRST label can be downloaded at %s" % transaction.label_url)
    # 

else:
    print("Failed purchasing the label due to:")
    for message in transaction.messages:
        print("- %s" % message['text'])

print("This is async so we need to get the transaction + rate_id once queded has changed (to retrieve the remaining labels)") 

RETRY_LIMIT = 60  # retry 60 times before giving up
RETRY_SLEEP = 0.5 
tries = 0

while transaction.status == 'QUEUED' and tries < RETRY_LIMIT:
    time.sleep(RETRY_SLEEP)
    transaction = shippo.Transaction.retrieve(transaction.object_id)
    tries += 1

if transaction.status == "SUCCESS":
    transactions = shippo.Transaction.all(transaction=transaction.object_id,rate=rate.object_id,size=len(parcel_list))
    for num,label in enumerate(transactions.results):
        print(f"\nPurchased label with tracking number {label.tracking_number}")
            
        print("Label {} can be downloaded at:\n\n {}".format(num + 1, label.label_url))
   
# For more tutorials of address validation, tracking, returns, refunds,
# and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
