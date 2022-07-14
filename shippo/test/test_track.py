# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import ShippoTestCase, DUMMY_TRANSACTION, create_mock_shipment

from shippo.test.helper import shippo_vcr


def create_transaction() -> shippo.Transaction:
    shipment = create_mock_shipment()
    # get_rates cannot be provided asynchronous=False, otherwise transaction will fail and have no tracking no
    rates = shippo.Shipment.get_rates(shipment.object_id)
    data = {
        'rate': rates.results[0].object_id,
        'label_file_type': 'PDF',
        'async': False,
    }
    transaction = shippo.Transaction.create(**data, asynchronous=False)
    return transaction


class TrackTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(TrackTests, self).setUp()
        self.tracking_number = '99991235604553255TEST'
        # self.transaction = create_transaction()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(TrackTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_get_status(self):
        carrier_token = 'usps'
        tracking = shippo.Track.get_status(carrier_token, self.tracking_number)
        self.assertTrue(tracking)
        self.assertTrue('tracking_status' in tracking)
        self.assertTrue('tracking_history' in tracking)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_invalid_get_status(self):
        self.assertRaises(
            shippo.error.InvalidRequestError,
            shippo.Track.get_status,
            'EXAMPLE_OF_INVALID_CARRIER',
            self.tracking_number
        )
        self.assertRaises(
            shippo.error.InvalidRequestError,
            shippo.Track.get_status,
            'shippo',
            'EXAMPLE_OF_INVALID_TRACKING_NUMBER'
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_create(self):
        tracking = shippo.Track.create(
            carrier='usps',
            tracking_number=self.tracking_number,
            metadata='metadata'
        )
        self.assertTrue(tracking)
        self.assertTrue('tracking_status' in tracking)
        self.assertTrue('tracking_history' in tracking)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_invalid_create(self):
        self.assertRaises(
            shippo.error.InvalidRequestError,
            shippo.Track.create,
            None,
            **{
                'carrier': 'EXAMPLE_OF_INVALID_CARRIER',
                'tracking_number': self.tracking_number,
                'metadata': 'metadata'
            }
        )
        tracking = shippo.Track.create(
            carrier='usps',
            tracking_number='EXAMPLEOFINVALID123TRACKINGNUMBER',
            metadata='metadata'
        )
        self.assertFalse(tracking.tracking_status)
        self.assertFalse(tracking.tracking_history)


if __name__ == '__main__':
    unittest2.main()
