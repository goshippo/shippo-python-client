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
        super(ParcelTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(ParcelTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Parcel.create, **INVALID_PARCEL)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_create(self):
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        self.assertEqual(parcel.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_retrieve(self):
        parcel = shippo.Parcel.create(**DUMMY_PARCEL)
        retrieve = shippo.Parcel.retrieve(parcel.object_id)
        self.assertItemsEqual(parcel, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Parcel.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_list_all(self):
        parcel_list = shippo.Parcel.all()
        self.assertTrue('count' in parcel_list)
        self.assertTrue('results' in parcel_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/parcel')
    def test_list_page_size(self):
        pagesize = 1
        parcel_list = shippo.Parcel.all(size=pagesize)
        self.assertEquals(len(parcel_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
