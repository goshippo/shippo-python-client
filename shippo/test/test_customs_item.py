# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_CUSTOMS_ITEM,
    INVALID_CUSTOMS_ITEM,
    ShippoTestCase,
)

from shippo.test.helper import shippo_vcr


class CustomsItemTest(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets the superapi.

        Args:
            self: (todo): write your description
        """
        super(CustomsItemTest, self).setUp()

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
        super(CustomsItemTest, self).tearDown()
        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_invalid_create(self):
        """
        Create the test **

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.InvalidRequestError, shippo.CustomsItem.create,
                          **INVALID_CUSTOMS_ITEM)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_create(self):
        """
        Create a new object.

        Args:
            self: (todo): write your description
        """
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        self.assertEqual(customs_item.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_retrieve(self):
        """
        Retrieves the item.

        Args:
            self: (todo): write your description
        """
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        retrieve = shippo.CustomsItem.retrieve(customs_item.object_id)
        self.assertItemsEqual(customs_item, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_invalid_retrieve(self):
        """
        Retrieve the test information for the given test.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError,
                          shippo.CustomsItem.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_list_all(self):
        """
        Test if a list of the library items

        Args:
            self: (todo): write your description
        """
        customs_items_list = shippo.CustomsItem.all()
        self.assertTrue('results' in customs_items_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-item')
    def test_list_page_size(self):
        """
        Lists all pages todos

        Args:
            self: (todo): write your description
        """
        pagesize = 1
        customs_items_list = shippo.CustomsItem.all(size=pagesize)
        self.assertEqual(len(customs_items_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
