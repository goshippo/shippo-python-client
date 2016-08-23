import shippo

# replace <API-KEY> with your key
shippo.api_key = "<API-KEY>"

###################
# Domestic Shipment
###################

#example address_from object dict
address_from = {
    "object_purpose":"PURCHASE",
    "name":"Mr Hippo",
    "company":"Shippo",
    "street1":"215 Clayton St.",
    "city":"San Francisco",
    "state":"CA",
    "zip":"94117",
    "country":"US",
    "phone":"+1 555 341 9393",
    "email":"mrhippo@goshippo.com",
}

# example address_to object dict
address_to = {
    "object_purpose":"PURCHASE",
    "name":"Ms Hippo",
    "company":"",
    "street1":"Broadway 1",
    "street2":"",
    "city":"New York",
    "state":"NY",
    "zip":"10007",
    "country":"US",
    "phone":"+1 555 341 9393",
    "email":"mshippo@goshippo.com",
    "metadata" : "Hippos dont lie"
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

#Creating the shipment object. In this example, the objects are directly passed to the
#Shipment.create method, Alternatively, the Address and Parcel objects could be created
#using Address.create(..) and Parcel.create(..) functions respectively.
shipment = shippo.Shipment.create(
    object_purpose= 'PURCHASE',
    address_from= address_from,
    address_to= address_to,
    parcel= parcel,
    async= False )

#Get the first rate in the rates results for demo purposes.
rate = shipment.rates_list[0]

#Purchase the desired rate.
transaction = shippo.Transaction.create(rate=rate.object_id, async=False)

#print label_url and tracking_number
if transaction.object_status == "SUCCESS":
    print "Purchased label with tracking number %s" % transaction.tracking_number
    print "The label can be downloaded at %s" % transaction.label_url
else:
    print "Failed purchasing the label due to:"
    for message in transaction.messages:
        print "- %s" % message['text']


########################
# International Shipment
########################

#example address_to object dict
address_to_international = {
    "object_purpose":"PURCHASE",
    "name":"Mr Hippo",
    "company":"London Zoo",
    "street1":"Regent's Park",
    "street2":"Outer Cir",
    "city":"LONDON",
    "zip":"NW1 4RY",
    "country":"GB",
    "phone":"+1 555 341 9393",
    "email":"mrhippo@goshippo.com",
    "metadata" : "Hippos dont lie"
}

#example CustomsItems object.
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

#Creating the CustomsDeclaration
customs_declaration = shippo.CustomsDeclaration.create(
    contents_type= 'MERCHANDISE',
    contents_explanation= 'T-Shirt purchase',
    non_delivery_option= 'RETURN',
    certify= True,
    certify_signer= 'Mr Hippo',
    items= [customs_item])

#Creating the shipment object. In this example, the objects are directly passed to the
#Shipment.create method, Alternatively, the Address and Parcel objects could be created
#using Address.create(..) and Parcel.create(..) functions respectively.
shipment_international = shippo.Shipment.create(
    object_purpose= 'PURCHASE',
    address_from= address_from,
    address_to= address_to_international,
    parcel= parcel,
    customs_declaration=customs_declaration.object_id,
    async= False )

#Get the first rate in the rates results for demo purposes.
rate_international = shipment_international.rates_list[0]

#Purchase the desired rate.
transaction_international = shippo.Transaction.create(rate=rate_international.object_id, async=False)

# print label_url and tracking_number
if transaction_international.object_status == "SUCCESS":
    print "Purchased label with tracking number %s" % transaction_international.tracking_number
    print "The label can be downloaded at %s" % transaction_international.label_url
else:
    print "Failed purchasing the label due to:"
    for message in transaction_international.messages:
        print "- %s" % message['text']
