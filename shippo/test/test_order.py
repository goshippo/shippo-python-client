# -*- coding: utf-8 -*-
import unittest2

from mock import patch
from datetime import datetime

import shippo
from shippo.test.helper import (
    ShippoTestCase,
    DUMMY_ORDER
)

from shippo.test.helper import shippo_vcr


class OrderTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(OrderTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(OrderTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError,
                          shippo.Order.create)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_create(self):
        ORDER = DUMMY_ORDER
        ORDER['placed_at'] = datetime.now().isoformat() + "Z"
        order = shippo.Order.create(**ORDER)
        self.assertEqual(order.order_status, 'PAID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_retrieve(self):
        ORDER = DUMMY_ORDER
        ORDER['placed_at'] = datetime.now().isoformat() + "Z"
        order = shippo.Order.create(**ORDER)
        retrieve = shippo.Order.retrieve(order.object_id)
        self.assertItemsEqual(order.object_id, retrieve.object_id)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError,
                          shippo.Order.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_list_all(self):
        order_list = shippo.Order.all()
        self.assertTrue('results' in order_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/order')
    def test_list_page_size(self):
        pagesize = 1
        order_list = shippo.Order.all(size=pagesize)
        self.assertEqual(len(order_list.results), pagesize)

if __name__ == '__main__':
    unittest2.main()
