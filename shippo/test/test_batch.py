# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    create_mock_shipment,
    ShippoTestCase,
    DUMMY_BATCH,
    INVALID_BATCH
)

from shippo.test.helper import shippo_vcr

BATCH_ADD_SIZE = 4


class BatchTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets the proxy.

        Args:
            self: (todo): write your description
        """
        super(BatchTests, self).setUp()

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
        super(BatchTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_create(self):
        """
        Creates a batch.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        self.assertEqual(batch.status, 'VALIDATING')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_invalid_create(self):
        """
        Create a test todo.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.InvalidRequestError,
                          shippo.Batch.create)
        INVALID = INVALID_BATCH.copy()
        self.assertRaises(
            shippo.error.InvalidRequestError,
            shippo.Batch.create,
            **INVALID
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_retrieve(self):
        """
        Retrieves the batch.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        retrieve = shippo.Batch.retrieve(batch.object_id)
        self.assertItemsEqual(batch, retrieve)
        # Leave enough time for the batch to be processed
        retrieve = shippo.Batch.retrieve(
            batch.object_id,
            **{
                'object_results': 'creation_succeeded'
            }
        )
        self.assertGreater(len(retrieve['batch_shipments']['results']), 0)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_invalid_retrieve(self):
        """
        Check if the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.APIError,
                          shippo.Batch.retrieve, 'EXAMPLE_OF_INVALID_ID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_add(self):
        """
        Adds a test to the batch.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        # Leave enough time for the batch to be processed
        retrieve = shippo.Batch.retrieve(batch.object_id)
        batch_size = len(retrieve.batch_shipments.results)
        self.assertEqual(batch.status, 'VALIDATING')
        addon = []
        for i in range(BATCH_ADD_SIZE):
            mock_shipment = create_mock_shipment()
            addon.append({'shipment': mock_shipment.object_id})
        added = shippo.Batch.add(batch.object_id, addon)
        added_size = len(added.batch_shipments.results)
        self.assertEqual(batch_size + len(addon), added_size)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_invalid_add(self):
        """
        Validate the test status.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        self.assertEqual(batch.status, 'VALIDATING')
        mock_shipment = create_mock_shipment()
        self.assertRaises(
            shippo.error.APIError,
            shippo.Batch.add,
            'INVALID_OBJECT_KEY',
            [{'shipment': [mock_shipment]}]
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_remove(self):
        """
        Removes a batch of items from the batch.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        # Leave enough time for the batch to be processed
        retrieve = shippo.Batch.retrieve(batch.object_id)
        batch_size = len(retrieve.batch_shipments.results)
        self.assertEqual(batch.status, 'VALIDATING')
        addon = []
        for i in range(BATCH_ADD_SIZE):
            mock_shipment = create_mock_shipment()
            addon.append({'shipment': mock_shipment.object_id})
        added = shippo.Batch.add(batch.object_id, addon)
        added_size = len(added.batch_shipments.results)
        self.assertEqual(batch_size + len(addon), added_size)
        to_remove = []
        for shipment in added.batch_shipments.results:
            to_remove.append(shipment.object_id)
        removed = shippo.Batch.remove(batch.object_id, to_remove)
        self.assertEqual(len(removed.batch_shipments.results), 0)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_invalid_remove(self):
        """
        Respond to see https : class : class.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        self.assertEqual(batch.status, 'VALIDATING')
        retrieve = shippo.Batch.retrieve(batch.object_id)
        to_remove = []
        for shipment in retrieve.batch_shipments.results:
            to_remove.append(shipment.object_id)
        self.assertRaises(
            shippo.error.APIError,
            shippo.Batch.add,
            'INVALID_OBJECT_KEY',
            to_remove
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_purchase(self):
        """
        Test if the batch is still running.

        Args:
            self: (todo): write your description
        """
        BATCH = DUMMY_BATCH.copy()
        batch = shippo.Batch.create(**BATCH)
        while batch.status == 'VALIDATING':
            batch = shippo.Batch.retrieve(batch.object_id)
        purchase = shippo.Batch.purchase(batch.object_id)
        self.assertEqual(purchase.status, 'PURCHASING')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/batch')
    def test_invalid_purchase(self):
        """
        Check if the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(
            shippo.error.APIError,
            shippo.Batch.purchase,
            'INVALID_OBJECT_ID'
        )


if __name__ == '__main__':
    unittest2.main()
