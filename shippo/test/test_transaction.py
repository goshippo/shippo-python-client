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
    NOW, DUMMY_TRANSACTION, INVALID_TRANSACTION
    )

class TransactionTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(TransactionTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(TransactionTests, self).tearDown()

        self.client_patcher.stop()
        
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Transaction.create)
                          
    def test_create(self):
        shipment = test_shipment.create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, sync=True)
        rate = rates.results[0]
        TRANSACTION = DUMMY_TRANSACTION.copy()
        TRANSACTION['rate']=rate.object_id
        transaction = shippo.Transaction.create(**TRANSACTION)
        self.assertEqual(transaction.object_state, 'VALID')
    
    def test_retrieve(self):
        shipment = test_shipment.create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, sync=True)
        rate = rates.results[0]
        TRANSACTION = DUMMY_TRANSACTION.copy()
        TRANSACTION['rate']=rate.object_id
        transaction = shippo.Transaction.create(**TRANSACTION)
        retrieve = shippo.Transaction.retrieve(transaction.object_id)
        self.assertItemsEqual(transaction, retrieve)
        
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Transaction.retrieve,
            'EXAMPLE_OF_INVALID_ID')
        
    def test_list_all(self):
        transaction_list = shippo.Transaction.all()
        self.assertTrue('count' in transaction_list)
        self.assertTrue('results' in transaction_list)
        
    def test_list_page_size(self):
        pagesize = 1
        transaction_list = shippo.Transaction.all(pagesize)
        self.assertEquals(len(transaction_list.results),pagesize)


if __name__ == '__main__':
    unittest.main()