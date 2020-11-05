# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_ADDRESS,
    DUMMY_MANIFEST,
    INVALID_MANIFEST,
    ShippoTestCase,
    create_mock_transaction,
    create_mock_manifest,
    create_mock_shipment
)

from shippo.test.helper import shippo_vcr


class ManifestTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets client. client.

        Args:
            self: (todo): write your description
        """
        super(ManifestTests, self).setUp()

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
        Stops the client.

        Args:
            self: (todo): write your description
        """
        super(ManifestTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_invalid_create(self):
        """
        Create a test to make sure that the resource.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(
            shippo.error.InvalidRequestError, shippo.Manifest.create,
            **INVALID_MANIFEST)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_create(self):
        """
        Create a new test.

        Args:
            self: (todo): write your description
        """
        transaction = create_mock_transaction()
        manifest = create_mock_manifest(transaction)
        self.assertEqual(manifest.status, 'SUCCESS')
        self.assertEqual(manifest.transactions[0], transaction.object_id)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_retrieve(self):
        """
        Retrieve the manifest for this manifest.

        Args:
            self: (todo): write your description
        """
        manifest = create_mock_manifest()
        retrieve = shippo.Manifest.retrieve(manifest.object_id)
        self.assertItemsEqual(manifest, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_invalid_retrieve(self):
        """
        Retrieve the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError, shippo.Manifest.retrieve,
                          'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_list_all(self):
        """
        Test if all manifest.

        Args:
            self: (todo): write your description
        """
        manifest_list = shippo.Manifest.all()
        self.assertTrue('results' in manifest_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/manifest')
    def test_list_page_size(self):
        """
        Return a list of all pages.

        Args:
            self: (todo): write your description
        """
        pagesize = 1
        manifest_list = shippo.Manifest.all(size=pagesize)
        self.assertEqual(len(manifest_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
