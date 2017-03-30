# Configurable variables
api_key = None
api_base = 'https://api.goshippo.com/'
api_version = None
verify_ssl_certs = True
rates_req_timeout = 20.0  # seconds

from shippo.resource import (
    Address,
    Batch,
    CarrierAccount,
    CustomsDeclaration,
    CustomsItem,
    Manifest,
    Parcel,
    Rate,
    Refund,
    Shipment,
    Track,
    Transaction,
)
