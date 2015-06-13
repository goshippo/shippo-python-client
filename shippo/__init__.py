# Configurable variables
api_key = None
api_base = 'https://api.goshippo.com/'
api_version = None
verify_ssl_certs = False
rates_req_timeout = 20.0  # seconds
transaction_req_timeout = 20.0 # seconds

from shippo.resource import (
    Address, Parcel, Shipment, CustomsItem, CustomsDeclaration, Manifest, Rate, Transaction, Refund)
