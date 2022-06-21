import shippo
import time

"""
In this tutorial we see how to use and interact with batches
"""

# Replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"

example_batch = {
    # replace with your carrier account
    "default_carrier_account": "<CARRIER-ACCOUNT>",
    # replace with desired service level, https://goshippo.com/docs/reference#servicelevels
    "default_servicelevel_token": "<SERVICE-LEVEL-TOKEN>",
    "label_filetype": "PDF_4x6",
    "metadata": "this is metadata",
    "batch_shipments": [
        {
            "shipment": {  # see basic-shipment.py on how to create shipments
                "address_from": {
                    "name": "Mr Hippo",
                    "street1": "965 Mission St",
                    "street2": "Ste 201",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94103",
                    "country": "US",
                    "phone": "4151234567",
                },
                "address_to": {
                    "name": "Mrs Hippo",
                    "company": "",
                    "street1": "Broadway 1",
                    "street2": "",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10007",
                    "country": "US",
                    "phone": "4151234567",
                },
                "parcels": [{
                    "length": "5",
                    "width": "5",
                    "height": "5",
                    "distance_unit": "in",
                    "weight": "2",
                    "mass_unit": "oz"
                }]
            }
        },
        {
            "shipment": {
                "address_from": {
                    "name": "Mr Hippo",
                    "street1": "1092 Indian Summer Ct",
                    "city": "San Jose",
                    "state": "CA",
                    "zip": "95122",
                    "country": "US",
                    "phone": "4151234567",
                },
                "address_to": {
                    "name": "Mrs Hippo",
                    "company": "",
                    "street1": "Broadway 1",
                    "street2": "",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10007",
                    "country": "US",
                    "phone": "4151234567",
                },
                "parcels": [{
                    "length": "5",
                    "width": "5",
                    "height": "5",
                    "distance_unit": "in",
                    "weight": "20",
                    "mass_unit": "lb"
                }]
            }
        }
    ]
}

# create batch, passing in each attribute as a parameter
batch = shippo.Batch.create(**example_batch)

"""
  The batch endpoint is async so we need to retrieve it in order to see the details
  In this example we are long-polling but in practice you should use webhooks over
    long-polling, we would encourage you to add a webhook through the UI
    see https://app.goshippo.com/api/
"""
batch = shippo.Batch.retrieve(batch.object_id)
tries = 0
TIMEOUT = 60  # thirty second timeout
while batch.status == 'VALIDATING' and tries < TIMEOUT:
    time.sleep(0.5)
    batch = shippo.Batch.retrieve(batch.object_id)
    tries += 1
print(batch)

# now we want to add a shipment to our batch
# create a sample shipment
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

address_to = {
    "name": "Shippo Friend",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}

parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb",
}

shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=[parcel],
    asynchronous=False
)

# the post data should be in an array even if it's just one shipment
# each shipment object_id should be in an dictionary as shown below
added = shippo.Batch.add(batch.object_id, [{'shipment': shipment.object_id}])
print(added)

# now let's remove a shipment from our batch
# find the object_id of the shipment you want to remove, it will not be the same as the id you used to add it
batch = shippo.Batch.retrieve(batch.object_id)
to_remove = []
for batch_shipment in batch.batch_shipments.results:
    # the shipment object_id is stored under the field 'shipment' in batch objects
    if shipment.object_id == batch_shipment.shipment:
        # but we used the batch object_id to remove it
        to_remove.append(batch_shipment.object_id)
# the post data here is just an array of ids
removed = shippo.Batch.remove(batch.object_id, to_remove)

# now we're ready to purchase
purchase = shippo.Batch.purchase(batch.object_id)
print(purchase)

# For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
