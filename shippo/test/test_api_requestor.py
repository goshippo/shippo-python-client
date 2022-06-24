
from shippo import api_requestor, config
from mock import patch, Mock
from unittest2 import TestCase
import unittest2
import sys

from shippo.api_requestor import APIRequestor
from shippo.config import config, Configuration
from shippo.error import ConfigurationError


class APIRequestorTests(TestCase):
    @patch.object(sys, 'version', '3.8.1 (default, Mar 13 2020, 20:31:03) \n[Clang 11.0.0 (clang-1100.0.33.17)]')
    def test_shippo_user_agent(self):
        configuration = Configuration()
        configuration.app_name = 'TestApp'
        configuration.app_version = '1.1.1'
        configuration.sdk_version = '0.0.0'

        actual = APIRequestor.get_shippo_user_agent_header(configuration=configuration)
        expected = 'TestApp/1.1.1 ShippoPythonSDK/0.0.0 Python/3.8.1'
        self.assertEqual(actual, expected)

    def test_oauth_token_auth(self):
        config.app_name = 'TestApp'
        config.app_version = '1.1.1'

        mock_client = Mock()
        mock_client.name = 'mock_client'
        mock_client.request.return_value = ('{"status": "ok"}', 200)

        requestor = api_requestor.APIRequestor(
            key='oauth.mocktoken.mocksig', client=mock_client)
        requestor.request('GET', '/v1/echo')

        args, kwargs = mock_client.request.call_args
        method, url, headers, data = args

        self.assertDictContainsSubset(
            {'Authorization': 'Bearer oauth.mocktoken.mocksig'},
            headers,
            "Expect correct token type to used for authorization with oauth token"
        )

    def test_shippo_token_auth(self):
        config.app_name = 'TestApp'
        config.app_version = '1.1.1'

        mock_client = Mock()
        mock_client.name = 'mock_client'
        mock_client.request.return_value = ('{"status": "ok"}', 200)

        requestor = api_requestor.APIRequestor(
            key='shippo_test_mocktoken', client=mock_client)
        requestor.request('GET', '/v1/echo')

        args, kwargs = mock_client.request.call_args
        method, url, headers, data = args

        self.assertDictContainsSubset(
            {'Authorization': 'ShippoToken shippo_test_mocktoken'},
            headers,
            "Expect correct token type to used for authorization with shippo token"
        )


if __name__ == '__main__':
    unittest2.main()
