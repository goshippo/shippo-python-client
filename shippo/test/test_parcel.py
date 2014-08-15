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
    NOW, DUMMY_PARCEL, INVALID_PARCEL
    )

class ParcelTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(ParcelTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(ParcelTests, self).tearDown()

        self.client_patcher.stop()
        
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Parcel.create,
                          INVALID_PARCEL)
                          
    def test_create(self):
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        self.assertEqual(parcel.object_state, 'VALID')
    
    def test_retrieve(self):
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        retrieve = shippo.Parcel.retrieve(parcel.object_id)
        self.assertItemsEqual(parcel, retrieve)
        
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Parcel.retrieve,
            'EXAMPLE_OF_INVALID_ID')
        
    def test_list_all(self):
        parcel_list = shippo.Parcel.all()
        self.assertTrue('count' in parcel_list)
        self.assertTrue('results' in parcel_list)
        
    def test_list_page_size(self):
        pagesize = 1
        parcel_list = shippo.Parcel.all(pagesize)
        self.assertEquals(len(parcel_list.results),pagesize)


if __name__ == '__main__':
    unittest.main()