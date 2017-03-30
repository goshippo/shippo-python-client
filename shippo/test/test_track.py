# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import ShippoTestCase

from shippo.test.helper import shippo_vcr


class TrackTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient
    usps_tracking_no = '9205590164917337534322'

    def setUp(self):
        super(TrackTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch('shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(TrackTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_get_status(self):
        carrier_token = 'usps'
        tracking = shippo.Track.get_status(carrier_token, self.usps_tracking_no)
        self.assertTrue(tracking)
        self.assertTrue('tracking_status' in tracking)
        self.assertTrue('tracking_history' in tracking)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_invalid_get_status(self):
        self.assertRaises(
            shippo.error.InvalidRequestError,
            shippo.Track.get_status,
            'EXAMPLE_OF_INVALID_CARRIER',
            self.usps_tracking_no
        )
        self.assertRaises(
            shippo.error.APIError,
            shippo.Track.get_status,
            'usps',
            'EXAMPLE_OF_INVALID_TRACKING_NUMBER'
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/track')
    def test_create(self):
        tracking = shippo.Track.create(
            carrier='usps',
            tracking_number=self.usps_tracking_no,
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
                'tracking_number': self.usps_tracking_no,
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
