# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_ADDRESS,
    INVALID_ADDRESS,
    NOT_POSSIBLE_ADDRESS,
    ShippoTestCase,
)

from shippo.test.helper import shippo_vcr


class AddressTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(AddressTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(AddressTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Address.create,
                          **INVALID_ADDRESS)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_create(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_retrieve(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        retrieve = shippo.Address.retrieve(address.object_id)
        self.assertItemsEqual(address, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Address.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_list_all(self):
        address_list = shippo.Address.all()
        self.assertTrue('count' in address_list)
        self.assertTrue('results' in address_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_list_page_size(self):
        pagesize = 1
        address_list = shippo.Address.all(size=pagesize)
        self.assertEquals(len(address_list.results), pagesize)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_validate(self):
        address = shippo.Address.create(**NOT_POSSIBLE_ADDRESS)
        self.assertEqual(address.object_state, 'VALID')
        address = shippo.Address.validate(address.object_id)
        self.assertEqual(address.object_source, 'VALIDATOR')
        self.assertEqual(address.object_state, 'INVALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_validate(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address.object_state, 'VALID')
        address = shippo.Address.validate(address.object_id)
        self.assertEqual(address.object_source, 'VALIDATOR')

if __name__ == '__main__':
    unittest2.main()
