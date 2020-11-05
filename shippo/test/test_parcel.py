# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_PARCEL,
    INVALID_PARCEL,
    ShippoTestCase,
)

from shippo.test.helper import shippo_vcr


class ParcelTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets the http proxy.

        Args:
            self: (todo): write your description
        """
        super(ParcelTests, self).setUp()

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
        super(ParcelTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_invalid_create(self):
        """
        Test that the test.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.InvalidRequestError,
                          shippo.Parcel.create, **INVALID_PARCEL)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_create(self):
        """
        Creates a test.

        Args:
            self: (todo): write your description
        """
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        self.assertEqual(parcel.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_retrieve(self):
        """
        Retrieve the test object for a test.

        Args:
            self: (todo): write your description
        """
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        retrieve = shippo.Parcel.retrieve(parcel.object_id)
        self.assertItemsEqual(parcel, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_invalid_retrieve(self):
        """
        Check if a test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError,
                          shippo.Parcel.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_list_all(self):
        """
        Assigns all test lists have a list.

        Args:
            self: (todo): write your description
        """
        parcel_list = shippo.Parcel.all()
        self.assertTrue('results' in parcel_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_list_page_size(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        pagesize = 2
        parcel_list = shippo.Parcel.all(size=pagesize)
        self.assertEqual(len(parcel_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
