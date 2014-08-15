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
    NOW, DUMMY_ADDRESS, INVALID_ADDRESS
    )
    
class FunctionalTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(FunctionalTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(FunctionalTests, self).tearDown()

        self.client_patcher.stop()

    def test_dns_failure(self):
        api_base = shippo.api_base
        try:
            shippo.api_base = 'https://my-invalid-domain.ireallywontresolve/v1'
            self.assertRaises(shippo.error.APIConnectionError,
                              shippo.Address.create)
        finally:
            shippo.api_base = api_base

    def test_run(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address.object_state, 'VALID')
        address= shippo.Address.validate(address.object_id)
        self.assertEqual(address.object_source, 'VALIDATOR')

    def test_list_accessors(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address['object_created'], address.object_created)
        address['foo'] = 'bar'
        self.assertEqual(address.foo, 'bar')

    def test_raise(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Address.create,
                          INVALID_ADDRESS)

    def test_unicode(self):
        # Make sure unicode requests can be sent
        self.assertRaises(shippo.error.APIError,
                          shippo.Address.retrieve,
                          u'☃')


    # --- if dynamic object typing is implemented, this will be a useful test
    # def test_missing_id(self):
    #     address = shippo.Address()
    #     self.assertRaises(shippo.error.APIError, address.refresh)
        


if __name__ == '__main__':
    unittest.main()