import shippo
import time

"""
In this tutorial we have an order with a sender address,
recipient address and parcel information that we need to ship.
"""

# Replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"
# replace <carrier_account> with carrier object_id 
carrier_account = "<carrier_account>"

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
    "length": "3",
    "width": "3",
    "height": "3",
    "distance_unit": "in",
    "weight": "1",
    "mass_unit": "lb",
}

# 10 pieces to the shipment
parcel_list = []
for parcel_piece in range(0,10):
    parcel_list.append(parcel)

print("We now have {} in this shipment!".format(len(parcel_list)))
carrier = [carrier_account]

# Example shipment object
# For complete reference to the shipment object: https://goshippo.com/docs/reference#shipments
# This object has asynchronous=False, indicating that the function will wait until all rates are generated before it returns.
# By default, Shippo handles responses asynchronously. However this will be depreciated soon. Learn more: https://goshippo.com/docs/async
shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=parcel_list,
    carrier_accounts=carrier,
    asynchronous=True
)

# Rates are stored in the `rates` array
# The details on the returned object are here: https://goshippo.com/docs/reference#rates
# Get the first rate in the rates results for demo purposes.
shipment_id = shipment.object_id
print(f"the shipment_id {shipment_id}")
rates = shippo.Shipment.get_rates(shipment.object_id)
print(rates.results)
for x,y in enumerate(rates.results):
    print(f"{x}: amount: {y['amount']},rate_object_id {y['object_id']}")
the_rate = int(input("select which rate you'd like by entering number"))
rate = rates.results[the_rate]
print("rate selected: \n\n {}".format(rate))
# Purchase the desired rate with a transaction request
# Set asynchronous=False, indicating that the function will wait until the carrier returns a shipping label before it returns
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

print("Remember that because this is multipiece we need to now get the transaction + rate_id to retrieve the remaining labels") 

TIMEOUT = 60  # thirty second timeout
tries = 0

while transaction.status == 'QUEUED' and tries < TIMEOUT:
    time.sleep(0.5)
    transaction = shippo.Transaction.retrieve(transaction.object_id)
    tries += 1

if transaction.status == "SUCCESS":
    transactions = shippo.Transaction.all(transaction=transaction.object_id,rate=rate.object_id,size=len(parcel_list))
    for num,label in enumerate(transactions.results):
        print(f"\nPurchased label with tracking number {label.tracking_number}")
            
        print("Label {} can be downloaded at:\n\n {}".format(num + 1, label.label_url))
   
# For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
