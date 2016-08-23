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
        super(ShipmentTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(ShipmentTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Shipment.create,
                          **INVALID_SHIPMENT)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_create(self):
        shipment = create_mock_shipment()
        self.assertEqual(shipment.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_retrieve(self):
        shipment = create_mock_shipment()
        retrieve = shippo.Shipment.retrieve(shipment.object_id)
        self.assertItemsEqual(shipment, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Shipment.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_list_all(self):
        shipment_list = shippo.Shipment.all()
        self.assertTrue('count' in shipment_list)
        self.assertTrue('results' in shipment_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_list_page_size(self):
        pagesize = 1
        shipment_list = shippo.Shipment.all(size=pagesize)
        self.assertEquals(len(shipment_list.results), pagesize)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_get_rate(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id)
        self.assertTrue('count' in rates)
        self.assertTrue('results' in rates)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_get_rates_blocking(self):
        shipment = create_mock_shipment()
        rates = shippo.Shipment.get_rates(shipment.object_id, async=False)
        self.assertTrue('count' in rates)
        self.assertTrue('results' in rates)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/shipment')
    def test_invalid_get_rate(self):
        # we are testing async=True in order to test the 2nd API call of the function
        self.assertRaises(shippo.error.APIError, shippo.Shipment.get_rates,
                          'EXAMPLE_OF_INVALID_ID', async=True)


if __name__ == '__main__':
    unittest2.main()
