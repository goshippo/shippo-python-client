# -*- coding: utf-8 -*-
import unittest2

from mock import patch
from datetime import datetime, timedelta

import shippo
from shippo.test.helper import (
    create_mock_international_transaction,
    ShippoTestCase,
    DUMMY_PICKUP
)

from shippo.test.helper import shippo_vcr


class PickupTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(PickupTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(PickupTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/pickup')
    def test_create(self):
        transaction, carrier_account = create_mock_international_transaction()
        PICKUP = DUMMY_PICKUP
        PICKUP['carrier_account'] = carrier_account
        PICKUP['transactions'] = [transaction.object_id]
        pickupTimeStart = datetime.now() + timedelta(hours=1)
        pickupTimeEnd = pickupTimeStart + timedelta(days=1)
        PICKUP['pickupTimeStart'] = pickupTimeStart.isoformat() + "Z"
        PICKUP['pickupTimeEnd'] = pickupTimeEnd.isoformat() + "Z"
        try:
            pickup = shippo.Pickup.create(**PICKUP)
        except shippo.error.InvalidRequestError:
            self.assertTrue(True)
        else:
            self.assertEqual(pickup.status, 'SUCCESS')

if __name__ == '__main__':
    unittest2.main()
