# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time
import unittest

from mock import patch
import test_shipment

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import shippo

from shippo.test.helper import (
    ShippoTestCase,
    NOW
    )

class RateTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(RateTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(RateTests, self).tearDown()

        self.client_patcher.stop()
    
    def test_retrieve(self):
        shipment = test_shipment.create_mock_shipment()
        rates = shippo.Shipment.get_shipping_rate_blocking(shipment.object_id)
        rate = rates.results[0]
        retrieve = shippo.Rate.retrieve(rate.object_id)
        self.assertItemsEqual(rate, retrieve)
        
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Rate.retrieve,
            'EXAMPLE_OF_INVALID_ID')
        
    def test_list_all(self):
        rate_list = shippo.Rate.all()
        self.assertTrue('count' in rate_list)
        self.assertTrue('results' in rate_list)
        
    def test_list_page_size(self):
        pagesize = 1
        rate_list = shippo.Rate.all(pagesize)
        self.assertEquals(len(rate_list.results),pagesize)


if __name__ == '__main__':
    unittest.main()