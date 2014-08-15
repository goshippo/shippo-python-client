# Configurable variables
# for testing purposes

api_key = None
auth = None
api_base = 'https://api.goshippo.com/'
api_version = None
verify_ssl_certs = False

from shippo.resource import (
    Address, Parcel, Shipment, CustomsItem, CustomsDeclaration, Manifest, Rate, Transaction, Refund )