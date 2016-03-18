# -*- coding: utf-8 -*-
import unittest

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_ADDRESS,
    DUMMY_MANIFEST,
    INVALID_MANIFEST,
    ShippoTestCase,
)

from shippo.util import shippo_vcr


class ManifestTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(ManifestTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(ManifestTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.Manifest.create, **INVALID_MANIFEST)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_create(self):
        manifest = shippo.Manifest.create(**self.create_valid_manifest())
        self.assertEqual(manifest.object_status, 'NOTRANSACTIONS')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_no_transaction_create(self):
        manifest = shippo.Manifest.create(**self.create_mock_manifest())
        self.assertEqual(manifest.object_status, 'NOTRANSACTIONS')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_retrieve(self):
        manifest = shippo.Manifest.create(**self.create_mock_manifest())
        retrieve = shippo.Manifest.retrieve(manifest.object_id)
        self.assertItemsEqual(manifest, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.Manifest.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_list_all(self):
        manifest_list = shippo.Manifest.all()
        self.assertTrue('count' in manifest_list)
        self.assertTrue('results' in manifest_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_list_page_size(self):
        pagesize = 1
        manifest_list = shippo.Manifest.all(size=pagesize)
        self.assertEquals(len(manifest_list.results), pagesize)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def create_mock_manifest(self):
        address = shippo.Address.create(**DUMMY_ADDRESS)
        MANIFEST = DUMMY_MANIFEST.copy()
        MANIFEST['address_from'] = address.object_id
        return MANIFEST

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def create_valid_manifest(self):
        transactions = shippo.Transaction.all()
        rate = shippo.Rate.retrieve(transactions.results[0].rate)
        shipment = shippo.Shipment.retrieve(rate.shipment)
        MANIFEST = DUMMY_MANIFEST.copy()
        MANIFEST['address_from'] = shipment.address_to
        return MANIFEST


if __name__ == '__main__':
    unittest.main()
