import shippo

# replace <API-KEY> with your key
shippo.api_key = "<API-KEY>"


# example address_from object dict
address_from = {
    "object_purpose": "PURCHASE",
    "name": "Laura Behrens Wu",
    "company": "Shippo",
    "street1": "215 Clayton St.",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94117",
    "country": "US",  # iso2 country code
    "phone": "+1 555 341 9393",
    "email": "laura@goshippo.com",
}

# example address_to object dict
address_to = {
    "object_purpose": "PURCHASE",
    "name": "Mr Hippo",
    "company": "London Zoo",
    "street1": "Regent's Park",
    "street2": "Outer Cir",
    "city": "LONDON",
    "state": "",
    "zip": "NW1 4RY",
    "country": "GB",  # iso2 country code
    "phone": "+1 555 341 9393",
    "email": "mrhippo@goshippo.com",
    "metadata": "Hippos dont lie"
}

# parcel object dict
parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb",
}

# example CustomsItems object. This is required for int'l shipment only.
customs_item = {
    "description": "T-Shirt",
    "quantity": 2,
    "net_weight": "400",
    "mass_unit": "g",
    "value_amount": "20",
    "value_currency": "USD",
    "origin_country": "US",
    "tariff_number": "",
}

# Creating the CustomsDeclaration
# (CustomsDeclaration are NOT required for domestic shipments)
customs_declaration = shippo.CustomsDeclaration.create(
    contents_type='MERCHANDISE',
    contents_explanation='T-Shirt purchase',
    non_delivery_option='RETURN',
    certify=True,
    certify_signer='Laura Behrens Wu',
    items=[customs_item]
)

# Creating the shipment object. In this example, the objects are directly passed to the
# Shipment.create method, Alternatively, the Address and Parcel objects could be created
# using Address.create(..) and Parcel.create(..) functions respectively.
shipment = shippo.Shipment.create(
    object_purpose='PURCHASE',
    address_from=address_from,
    address_to=address_to,
    parcel=parcel,
    submission_type='DROPOFF',
    customs_declaration=customs_declaration.object_id
)

# Get all rates for shipment. sync=True indicates that the function will wait until all
# rates are generated before it returns
rates = shippo.Shipment.get_rates(shipment.object_id, sync=True)

# Get the first rate in the rates results for demo purposes.
rate = rates.results[0]

# Purchase the desired rate. sync=True indicates that the function will wait until the
# carrier returns a shipping label before it returns
transaction = shippo.Transaction.create(rate=rate.object_id, sync=True)

# print label_url and tracking_number
if transaction.object_status == "SUCCESS":
    print transaction.label_url
    print transaction.tracking_number
else:
    print transaction.messages
