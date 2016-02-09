# Configurable variables
api_key = None
api_base = 'https://api.goshippo.com/'
api_version = None
verify_ssl_certs = False

from shippo.resource import (
    Address,
    CarrierAccount,
    CustomsDeclaration,
    CustomsItem,
    Manifest,
    Parcel,
    Rate,
    Refund,
    Shipment,
    Transaction,
)
