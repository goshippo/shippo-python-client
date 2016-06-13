# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    create_mock_shipment,
    ShippoTestCase,
    DUMMY_TRANSACTION
)

from shippo.test.helper import shippo_vcr


class TransactionTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(TransactionTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch('shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(TransactionTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Transaction.create)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_create(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, async=False)
        rate = rates.results[0]
        TRANSACTION = DUMMY_TRANSACTION.copy()
        TRANSACTION['rate'] = rate.object_id
        transaction = shippo.Transaction.create(**TRANSACTION)
        self.assertEqual(transaction.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_retrieve(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, async=False)
        rate = rates.results[0]
        TRANSACTION = DUMMY_TRANSACTION.copy()
        TRANSACTION['rate'] = rate.object_id
        transaction = shippo.Transaction.create(**TRANSACTION)
        retrieve = shippo.Transaction.retrieve(transaction.object_id)
        self.assertItemsEqual(transaction, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Transaction.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_list_all(self):
        transaction_list = shippo.Transaction.all()
        self.assertTrue('count' in transaction_list)
        self.assertTrue('results' in transaction_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/transaction')
    def test_list_page_size(self):
        pagesize = 1
        transaction_list = shippo.Transaction.all(size=pagesize)
        self.assertEquals(len(transaction_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
