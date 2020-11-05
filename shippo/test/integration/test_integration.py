# -*- coding: utf-8 -*-
import unittest2

from mock import patch

import shippo
from shippo.test.helper import (
    create_mock_shipment,
    DUMMY_ADDRESS,
    INVALID_ADDRESS,
    ShippoTestCase,
)


class FunctionalTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        """
        Sets the client.

        Args:
            self: (todo): write your description
        """
        super(FunctionalTests, self).setUp()

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
        super(FunctionalTests, self).tearDown()

        self.client_patcher.stop()

    def test_dns_failure(self):
        """
        Test if the dnso dns.

        Args:
            self: (todo): write your description
        """
        api_base = shippo.config.api_base
        try:
            shippo.config.api_base = 'https://my-invalid-domain.ireallywontresolve/v1'
            self.assertRaises(shippo.error.APIConnectionError,
                              shippo.Address.create)
        finally:
            shippo.config.api_base = api_base

    def test_run(self):
        """
        Test if the test.

        Args:
            self: (todo): write your description
        """
        try:
            address = shippo.Address.create(**DUMMY_ADDRESS)
            self.assertEqual(address.is_complete, True)
            address_validated = shippo.Address.validate(address.object_id)
            self.assertEqual(address_validated.is_complete, True)
        except shippo.error.AuthenticationError:
            self.fail('Set your SHIPPO_API_KEY in your os.environ')
        except Exception as inst:
            self.fail("Test failed with exception %s" % inst)

    def test_list_accessors(self):
        """
        Add accessors.

        Args:
            self: (todo): write your description
        """
        try:
            address = shippo.Address.create(**DUMMY_ADDRESS)
        except shippo.error.AuthenticationError:
            self.fail('Set your SHIPPO_API_KEY in your os.environ')

        self.assertEqual(address['object_created'], address.object_created)
        address['foo'] = 'bar'
        self.assertEqual(address.foo, 'bar')

    def test_unicode(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        # Make sure unicode requests can be sent
        self.assertRaises(shippo.error.APIError,
                          shippo.Address.retrieve,
                          '☃')

    def test_get_rates(self):
        """
        Test if the test is_ratesment.

        Args:
            self: (todo): write your description
        """
        try:
            shipment = create_mock_shipment()
            rates = shippo.Shipment.get_rates(
                shipment.object_id, asynchronous=False)
        except shippo.error.InvalidRequestError:
            pass
        except shippo.error.AuthenticationError:
            self.fail('Set your SHIPPO_API_KEY in your os.environ')
        except Exception as inst:
            self.fail("Test failed with exception %s" % inst)
        self.assertTrue('results' in rates)

    # --- if dynamic object typing is implemented, this will be a useful test
    # def test_missing_id(self):
    #     address = shippo.Address()
    #     self.assertRaises(shippo.error.APIError, address.refresh)


if __name__ == '__main__':
    unittest2.main()
