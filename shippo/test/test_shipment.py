# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time
import unittest

from mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import shippo

from shippo.test.helper import (
    ShippoTestCase,
    NOW, DUMMY_SHIPMENT, INVALID_SHIPMENT, TO_ADDRESS, FROM_ADDRESS, DUMMY_PARCEL
    )

class ShipmentTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(ShipmentTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(ShipmentTests, self).tearDown()

        self.client_patcher.stop()
        
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Shipment.create,
                          INVALID_SHIPMENT)
                          
    def test_create(self):
        shipment = create_mock_shipment()
        self.assertEqual(shipment.object_state, 'VALID')
    
    def test_retrieve(self):
        shipment = create_mock_shipment()
        retrieve = shippo.Shipment.retrieve(shipment.object_id)
        self.assertItemsEqual(shipment, retrieve)
        
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Shipment.retrieve,
                          'EXAMPLE_OF_INVALID_ID')
        
    def test_list_all(self):
        shipment_list = shippo.Shipment.all()
        self.assertTrue('count' in shipment_list)
        self.assertTrue('results' in shipment_list)
        
    def test_list_page_size(self):
        pagesize = 1
        shipment_list = shippo.Shipment.all(pagesize)
        self.assertEquals(len(shipment_list.results),pagesize)
        
    def test_get_rate(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id)
        self.assertTrue('count' in rates)
        self.assertTrue('results' in rates)
        
    def test_get_rates_blocking(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, sync=True)
        self.assertTrue('count' in rates)
        self.assertTrue('results' in rates)
    
    def test_invalid_get_rate(self):
        self.assertRaises(shippo.error.APIError, shippo.Shipment.get_rates,
                              'EXAMPLE_OF_INVALID_ID')
        
def create_mock_shipment():
    to_address = shippo.Address.create(**TO_ADDRESS)
    from_address = shippo.Address.create(**FROM_ADDRESS)
    parcel = shippo.Parcel.create(**DUMMY_PARCEL)
    SHIPMENT = DUMMY_SHIPMENT.copy()
    SHIPMENT['address_from']=from_address.object_id
    SHIPMENT['address_to']=to_address.object_id
    SHIPMENT['parcel']=parcel.object_id
    shipment = shippo.Shipment.create(**SHIPMENT)
    return shipment

def create_mock_international_shipment():
    SHIPMENT = self.create_mock_shipment()
    customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
    customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
    customs_declaration_parameters["items"][0] = customs_item.object_id
    customs_declaration = shippo.CustomsDeclaration.create(**customs_declaration_parameters)
    SHIPMENT['customs_declaration']=customs_declaration.object_id
    shipment = shippo.Shipment.create(**SHIPMENT)
    return shipment


if __name__ == '__main__':
    unittest.main()