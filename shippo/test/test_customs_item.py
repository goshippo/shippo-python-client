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
    NOW, DUMMY_CUSTOMS_ITEM, INVALID_CUSTOMS_ITEM
    )

class CustomsItemTest(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(CustomsItemTest, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(CustomsItemTest, self).tearDown()
        self.client_patcher.stop()
   
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.CustomsItem.create, 
            INVALID_CUSTOMS_ITEM)
                          
    def test_create(self):
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        self.assertEqual(customs_item.object_state, 'VALID')

    def test_retrieve(self):
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        retrieve = shippo.CustomsItem.retrieve(customs_item.object_id)
        self.assertItemsEqual(customs_item, retrieve)

    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.CustomsItem.retrieve, 
            'EXAMPLE_OF_INVALID_ID')

    def test_list_all(self):
        customs_items_list = shippo.CustomsItem.all()
        self.assertTrue('count' in customs_items_list)
        self.assertTrue('results' in customs_items_list)

    def test_list_page_size(self):
        pagesize = 1
        customs_items_list = shippo.CustomsItem.all(pagesize)
        self.assertEquals(len(customs_items_list.results),pagesize)


if __name__ == '__main__':
    unittest.main()