
from shippo import api_requestor
from mock import patch, Mock
from unittest2 import TestCase
import unittest2


class APIRequestorTests(TestCase):

    def test_oauth_token_auth(self):
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
