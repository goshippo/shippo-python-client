# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    create_mock_shipment,
    INVALID_SHIPMENT,
    ShippoTestCase,
)

from shippo.test.helper import shippo_vcr


class ShipmentTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets the client.

        Args:
            self: (todo): write your description
        """
        super(ShipmentTests, self).setUp()

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
        super(ShipmentTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_create(self):
        """
        Ensure that the test.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Shipment.create,
                          **INVALID_SHIPMENT)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_create(self):
        """
        Create a test test.

        Args:
            self: (todo): write your description
        """
        shipment = create_mock_shipment()
        self.assertEqual(shipment.status, 'SUCCESS')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_retrieve(self):
        """
        Retrieves the test.

        Args:
            self: (todo): write your description
        """
        shipment = create_mock_shipment()
        retrieve = shippo.Shipment.retrieve(shipment.object_id)
        self.assertItemsEqual(shipment, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_retrieve(self):
        """
        Check if the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError, shippo.Shipment.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_list_all(self):
        """
        Takes a test list

        Args:
            self: (todo): write your description
        """
        shipment_list = shippo.Shipment.all()
        self.assertTrue('results' in shipment_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_list_page_size(self):
        """
        List all pages in the list.

        Args:
            self: (todo): write your description
        """
        pagesize = 1
        shipment_list = shippo.Shipment.all(size=pagesize)
        self.assertEqual(len(shipment_list.results), pagesize)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_get_rate(self):
        """
        Set the test rate.

        Args:
            self: (todo): write your description
        """
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id)
        self.assertTrue('results' in rates)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_get_rates_blocking(self):
        """
        Set the rates for rates

        Args:
            self: (todo): write your description
        """
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(
            shipment.object_id, asynchronous=False)
        self.assertTrue('results' in rates)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_get_rate(self):
        """
        Test if the test rate.

        Args:
            self: (todo): write your description
        """
        # we are testing asynchronous=True in order to test the 2nd API call of the function
        self.assertRaises(shippo.error.APIError, shippo.Shipment.get_rates,
                          'EXAMPLE_OF_INVALID_ID', asynchronous=True)


if __name__ == '__main__':
    unittest2.main()
