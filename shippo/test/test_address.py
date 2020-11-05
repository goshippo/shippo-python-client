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
        """
        Sets the client to use.

        Args:
            self: (todo): write your description
        """
        super(AddressTests, self).setUp()

        def get_http_client(*args, **kwargs):
            """
            Return the http client.

            Args:
            """
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        """
        Stop the client.

        Args:
            self: (todo): write your description
        """
        super(AddressTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_create(self):
        """
        Create a test address.

        Args:
            self: (todo): write your description
        """
        address = shippo.Address.create(**INVALID_ADDRESS)
        self.assertEqual(address.is_complete, False)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_create(self):
        """
        Create a test test.

        Args:
            self: (todo): write your description
        """
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address.is_complete, True)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_retrieve(self):
        """
        Retrieve the shippo.

        Args:
            self: (todo): write your description
        """
        address = shippo.Address.create(**DUMMY_ADDRESS)
        retrieve = shippo.Address.retrieve(address.object_id)
        self.assertItemsEqual(address, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_retrieve(self):
        """
        Retrieve the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError, shippo.Address.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_list_all(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        address_list = shippo.Address.all()
        self.assertTrue('results' in address_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_list_page_size(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        pagesize = 1
        address_list = shippo.Address.all(size=pagesize)
        self.assertEqual(len(address_list.results), pagesize)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_invalid_validate(self):
        """
        Check if the test is valid.

        Args:
            self: (todo): write your description
        """
        address = shippo.Address.create(**NOT_POSSIBLE_ADDRESS)
        self.assertEqual(address.is_complete, True)
        address = shippo.Address.validate(address.object_id)
        self.assertEqual(address.is_complete, False)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/address')
    def test_validate(self):
        """
        Validate the test.

        Args:
            self: (todo): write your description
        """
        address = shippo.Address.create(**DUMMY_ADDRESS)
        self.assertEqual(address.is_complete, True)
        address = shippo.Address.validate(address.object_id)


if __name__ == '__main__':
    unittest2.main()
