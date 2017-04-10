import datetime
import os
import re
import shippo
import vcr

from mock import patch, Mock
from unittest2 import TestCase

NOW = datetime.datetime.now()

DUMMY_ADDRESS = {
    "name": "Laura Behrens Wu",
    "company": "Shippo",
    "street1": "Clayton St.",
    "street_no": "215",
    "street2": "",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94117",
    "country": "US",
    "phone": "+1 555 341 9393",
    "metadata": "Customer ID 123456"
}
INVALID_ADDRESS = {
    "name": "Laura Behrens Wu",
    "company": "Shippo",
    "street2": "",
    "city": "San Francisco",
    "state": "CA",
    "country": "US",
    "phone": "+1 555 341 9393",
    "metadata": "Customer ID 123456"
}
NOT_POSSIBLE_ADDRESS = {
    "name": "Laura Behrens Wu",
    "company": "Shippo",
    "street1": "ClaytonKLJLKJL St.",
    "street_no": "0798987987987",
    "street2": "",
    "city": "San Francisco",
    "state": "CA",
    "zip": "74338",
    "country": "US",
    "phone": "+1 555 341 9393",
    "metadata": "Customer ID 123456"
}
DUMMY_PARCEL = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "cm",
    "weight": "2",
    "mass_unit": "lb",
    "template": "",
    "metadata": "Customer ID 123456"
}
INVALID_PARCEL = {
    "length": "5",
    "width": "5",
    "distance_unit": "cm",
    "weight": "2",
    "template": "",
    "metadata": "Customer ID 123456"
}
DUMMY_MANIFEST = {
    "provider": "USPS",
    "shipment_date": "2017-03-31T17:37:59.817Z",
    "address_from": "28828839a2b04e208ac2aa4945fbca9a"
}
INVALID_MANIFEST = {
    "provider": "RANDOM_INVALID_PROVIDER",
    "shipment_date": "2014-05-16T23:59:59Z",
    "address_from": "EXAMPLE_OF_INVALID_ADDRESS"
}
DUMMY_CUSTOMS_ITEM = {
    "description": "T-Shirt",
    "quantity": 2,
    "net_weight": "400",
    "mass_unit": "g",
    "value_amount": "20",
    "value_currency": "USD",
    "tariff_number": "",
    "origin_country": "US",
    "metadata": "Order ID #123123"
}
INVALID_CUSTOMS_ITEM = {
    "value_currency": "USD",
    "tariff_number": "",
    "origin_country": "US",
    "metadata": "Order ID #123123"
}
DUMMY_CUSTOMS_DECLARATION = {
    "exporter_reference": "",
    "importer_reference": "",
    "contents_type": "MERCHANDISE",
    "contents_explanation": "T-Shirt purchase",
    "invoice": "#123123",
    "license": "",
    "certificate": "",
    "notes": "",
    "eel_pfc": "NOEEI_30_37_a",
    "aes_itn": "",
    "non_delivery_option": "ABANDON",
    "certify": True,
    "certify_signer": "Laura Behrens Wu",
    "disclaimer": "",
    "incoterm": "",
    "items": [
        "0c1a723687164307bb2175972fbcd9ef"
    ],
    "metadata": "Order ID #123123"
}
INVALID_CUSTOMS_DECLARATION = {
    "exporter_reference": "",
    "importer_reference": "",
    "contents_type": "MERCHANDISE",
    "contents_explanation": "T-Shirt purchase",
    "invoice": "#123123",
    "license": "",
    "certificate": "",
    "notes": "",
    "eel_pfc": "NOEEI_30_37_a",
    "aes_itn": "",
    "non_delivery_option": "ABANDON",
    "cerfy": True,
    "certify_signer": "Laura Behrens Wu",
    "disclaimer": "",
    "incoterm": "",
    "metadata": "Order ID #123123"
}
TO_ADDRESS = {
    "name": "John Smith",
    "company": "Initech",
    "street1": "965 Mission Street",
    "street_no": "",
    "street2": "Ste 480",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94103",
    "country": "US",
    "phone": "+1 630 333 7333",
    "metadata": "Customer ID 123456"
}
FROM_ADDRESS = {
    "name": "Laura Behrens Wu",
    "company": "Shippo",
    "street1": "Clayton St.",
    "street_no": "215",
    "street2": "",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94117",
    "country": "US",
    "phone": "+1 555 341 9393",
    "metadata": "Customer ID 123456"
}
DUMMY_SHIPMENT = {
    "address_from": "4f406a13253945a8bc8deb0f8266b245",
    "address_to": "4c7185d353764d0985a6a7825aed8ffb",
    "parcels": ["ec952343dd4843c39b42aca620471fd5"],
    "submission_type": "PICKUP",
    "shipment_date": "2017-03-31T17:37:59.817Z",
    "insurance_amount": "200",
    "insurance_currency": "USD",
    "extra": {
        "signature_confirmation": True,
        "reference_1": "",
        "reference_2": "",
        "insurance": {
            "amount": "200",
            "currency": "USD"
        }
    },
    "metadata": "Customer ID 123456"
}
INVALID_SHIPMENT = {
    "address_from": "4f406a13253945a8bc8deb0f8266b245",
    "submission_type": "PICKUP",
    "shipment_date": "2017-03-31T17:37:59.817Z",
    "extra": {
        "signature_confirmation": True,
        "reference_1": "",
        "reference_2": "",
        "insurance": {
            "amount": "200",
            "currency": "USD"
        }
    },
    "customs_declaration": "b741b99f95e841639b54272834bc478c",
    "metadata": "Customer ID 123456"
}
DUMMY_TRANSACTION = {
    "rate": "67891d0ebaca4973ae2569d759da6139",
    "metadata": "Customer ID 123456"
}
INVALID_TRANSACTION = {
    "metadata": "Customer ID 123456"
}
DUMMY_BATCH = {
    "default_carrier_account": "e68e95b95e33431a87bdecdd2b891c2b",
    "default_servicelevel_token": "usps_priority",
    "label_filetype": "PDF_4x6",
    "metadata": "BATCH #170",
    "batch_shipments": [
        {
          "shipment": {    
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
              "weight": "2",
              "mass_unit": "oz"
            }]
          }
        }
    ]
}
INVALID_BATCH = {
    "default_carrier_account": "NOT_VALID",
    "default_servicelevel_token": "usps_priority",
    "label_filetype": "PDF_4x6",
    "metadata": "teehee",
    "batch_shipments": []
}


def create_mock_shipment(async=False, api_key=None):
    to_address = shippo.Address.create(api_key=api_key, **TO_ADDRESS)
    from_address = shippo.Address.create(api_key=api_key, **FROM_ADDRESS)
    parcel = shippo.Parcel.create(api_key=api_key, **DUMMY_PARCEL)
    SHIPMENT = DUMMY_SHIPMENT.copy()
    SHIPMENT['address_from'] = from_address.object_id
    SHIPMENT['address_to'] = to_address.object_id
    SHIPMENT['parcels'] = [parcel.object_id]
    SHIPMENT['async'] = async
    shipment = shippo.Shipment.create(api_key=api_key, **SHIPMENT)
    return shipment


def create_mock_manifest(transaction=None):
    if not transaction:
        transaction = create_mock_transaction()
    rate = shippo.Rate.retrieve(transaction.rate)
    shipment = shippo.Shipment.retrieve(rate.shipment)
    MANIFEST = DUMMY_MANIFEST.copy()
    MANIFEST['address_from'] = shipment.address_from
    MANIFEST['async'] = False
    manifest = shippo.Manifest.create(**MANIFEST)
    return manifest


def create_mock_transaction(async=False):
    shipment = create_mock_shipment(async)
    rates = shipment.rates
    usps_rate = list(filter(lambda x: x.servicelevel.token == 'usps_priority', rates))[0]
    t = DUMMY_TRANSACTION.copy()
    t['rate'] = usps_rate.object_id
    t['async'] = async
    txn = shippo.Transaction.create(**t)
    return txn


def create_mock_international_shipment():
    SHIPMENT = create_mock_shipment()
    customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
    customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
    customs_declaration_parameters["items"][0] = customs_item.object_id
    customs_declaration = shippo.CustomsDeclaration.create(**customs_declaration_parameters)
    SHIPMENT['customs_declaration'] = customs_declaration.object_id
    shipment = shippo.Shipment.create(**SHIPMENT)
    return shipment


class ShippoTestCase(TestCase):
    RESTORE_ATTRIBUTES = ('api_version', 'api_key')

    def setUp(self):
        super(ShippoTestCase, self).setUp()

        self._shippo_original_attributes = {}

        for attr in self.RESTORE_ATTRIBUTES:
            self._shippo_original_attributes[attr] = getattr(shippo, attr)

        api_base = os.environ.get('SHIPPO_API_BASE')
        if api_base:
            shippo.api_base = api_base

        shippo.api_key = os.environ.get('SHIPPO_API_KEY', '51895b669caa45038110fd4074e61e0d')
        shippo.api_version = os.environ.get('SHIPPO_API_VERSION', '2017-03-29')

    def tearDown(self):
        super(ShippoTestCase, self).tearDown()

        for attr in self.RESTORE_ATTRIBUTES:
            setattr(shippo, attr, self._shippo_original_attributes[attr])

    # Python < 2.7 compatibility
    def assertRaisesRegexp(self, exception, regexp, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
        except exception, err:
            if regexp is None:
                return True

            if isinstance(regexp, basestring):
                regexp = re.compile(regexp)
            if not regexp.search(str(err)):
                raise self.failureException('"%s" does not match "%s"' %
                                            (regexp.pattern, str(err)))
        else:
            raise self.failureException(
                '%s was not raised' % (exception.__name__,))


class ShippoUnitTestCase(ShippoTestCase):
    REQUEST_LIBRARIES = ['urlfetch', 'requests']

    def setUp(self):
        super(ShippoUnitTestCase, self).setUp()

        self.request_patchers = {}
        self.request_mocks = {}
        for lib in self.REQUEST_LIBRARIES:
            patcher = patch("shippo.http_client.%s" % (lib,))

            self.request_mocks[lib] = patcher.start()
            self.request_patchers[lib] = patcher

    def tearDown(self):
        super(ShippoUnitTestCase, self).tearDown()

        for patcher in self.request_patchers.itervalues():
            patcher.stop()


class ShippoApiTestCase(ShippoTestCase):

    def setUp(self):
        super(ShippoApiTestCase, self).setUp()

        self.requestor_patcher = patch('shippo.api_requestor.APIRequestor')
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

    def tearDown(self):
        super(ShippoApiTestCase, self).tearDown()

        self.requestor_patcher.stop()

    def mock_response(self, res):
        self.requestor_mock.request = Mock(return_value=(res, 'reskey'))


shippo_vcr = vcr.VCR(
    filter_headers=['Authorization']
)
