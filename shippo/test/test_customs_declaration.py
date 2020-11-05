# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    DUMMY_CUSTOMS_DECLARATION,
    INVALID_CUSTOMS_DECLARATION,
    DUMMY_CUSTOMS_ITEM,
    ShippoTestCase,
)

from shippo.test.helper import shippo_vcr


class CustomsDeclarationTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Initializes this client.

        Args:
            self: (todo): write your description
        """
        super(CustomsDeclarationTests, self).setUp()

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
        super(CustomsDeclarationTests, self).tearDown()

        self.client_patcher.stop()

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_invalid_create(self):
        """
        Ensure that the test.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(shippo.error.InvalidRequestError, shippo.CustomsDeclaration.create,
                          **INVALID_CUSTOMS_DECLARATION)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_create(self):
        """
        Create a new object

        Args:
            self: (todo): write your description
        """
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
        customs_declaration_parameters["items"][0] = customs_item.object_id
        CustomsDeclaration = shippo.CustomsDeclaration.create(
            **customs_declaration_parameters)
        self.assertEqual(CustomsDeclaration.object_state, 'VALID')

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_retrieve(self):
        """
        Retrieve a single item

        Args:
            self: (todo): write your description
        """
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
        customs_declaration_parameters["items"][0] = customs_item.object_id
        CustomsDeclaration = shippo.CustomsDeclaration.create(
            **customs_declaration_parameters)
        # Test Retrieving Object
        retrieve = shippo.CustomsDeclaration.retrieve(
            CustomsDeclaration.object_id)
        self.assertItemsEqual(CustomsDeclaration, retrieve)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_invalid_retrieve(self):
        """
        Retrieve the test is valid.

        Args:
            self: (todo): write your description
        """
        self.assertRaises(
            shippo.error.APIError,
            shippo.CustomsDeclaration.retrieve,
            'EXAMPLE_OF_INVALID_ID'
        )

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_list_all(self):
        """
        Test if all custom declarations.

        Args:
            self: (todo): write your description
        """
        customs_declaration_list = shippo.CustomsDeclaration.all()
        self.assertTrue('results' in customs_declaration_list)

    @shippo_vcr.use_cassette(cassette_library_dir='shippo/test/fixtures/customs-declaration')
    def test_list_page_size(self):
        """
        Lists all the pages

        Args:
            self: (todo): write your description
        """
        pagesize = 1
        customs_declaration_list = shippo.CustomsDeclaration.all(size=pagesize)
        self.assertEqual(len(customs_declaration_list.results), pagesize)


if __name__ == '__main__':
    unittest2.main()
