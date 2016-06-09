import warnings
import unittest2

from mock import Mock
import shippo

from shippo.test.helper import ShippoUnitTestCase

VALID_API_METHODS = ('get', 'post', 'delete')


class HttpClientTests(ShippoUnitTestCase):

    def setUp(self):
        super(HttpClientTests, self).setUp()

        self.original_filters = warnings.filters[:]
        warnings.simplefilter('ignore')

    def tearDown(self):
        warnings.filters = self.original_filters

        super(HttpClientTests, self).tearDown()

    def check_default(self, none_libs, expected):
        for lib in none_libs:
            setattr(shippo.http_client, lib, None)

        inst = shippo.http_client.new_default_http_client()

        self.assertTrue(isinstance(inst, expected))

    def test_new_default_http_client_urlfetch(self):
        self.check_default((), shippo.http_client.UrlFetchClient)

    def test_new_default_http_client_requests(self):
        self.check_default(('urlfetch',), shippo.http_client.RequestsClient)


class ClientTestBase():

    @property
    def request_mock(self):
        return self.request_mocks[self.request_client.name]

    @property
    def valid_url(self, path='/v1/echo'):
        return 'https://api.goshippo.com%s' % (path,)

    def make_request(self, method, url, headers, post_data):
        client = self.request_client(verify_ssl_certs=True)
        return client.request(method, url, headers, post_data)

    def mock_response(self, body, code):
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def mock_error(self, error):
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def check_call(self, meth, abs_url, headers, params):
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def test_request(self):
        self.mock_response(self.request_mock, '{"status": "ok"}', 200)

        for meth in VALID_API_METHODS:
            abs_url = self.valid_url
            data = ''

            if meth != 'post':
                data = None

            headers = {'my-header': 'header val'}

            body, code = self.make_request(
                meth, abs_url, headers, data)

            self.assertEqual(200, code)
            self.assertEqual('{"status": "ok"}', body)

            # self.check_call(self.request_mock, meth, abs_url,
            #                 data, headers)

    def test_exception(self):
        self.mock_error(self.request_mock)
        self.assertRaises(shippo.error.APIConnectionError,
                          self.make_request,
                          'get', self.valid_url, {}, None)


class RequestsVerify(object):

    def __eq__(self, other):
        return other and other.endswith('shippo/data/ca-certificates.crt')


class RequestsClientTests(ShippoUnitTestCase, ClientTestBase):
    request_client = shippo.http_client.RequestsClient

    def mock_response(self, mock, body, code):
        result = Mock()
        result.content = body
        result.status_code = code

        mock.request = Mock(return_value=result)

    def mock_error(self, mock):
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, mock, meth, url, post_data, headers):
        mock.request.assert_called_with(meth, url,
                                        headers=headers,
                                        data=post_data,
                                        verify=RequestsVerify(),
                                        timeout=80)


class UrlFetchClientTests(ShippoUnitTestCase, ClientTestBase):
    request_client = shippo.http_client.UrlFetchClient

    def mock_response(self, mock, body, code):
        result = Mock()
        result.content = body
        result.status_code = code

        mock.fetch = Mock(return_value=result)

    def mock_error(self, mock):
        mock.Error = mock.InvalidURLError = Exception
        mock.fetch.side_effect = mock.InvalidURLError()

    def check_call(self, mock, meth, url, post_data, headers):
        mock.fetch.assert_called_with(
            url=url,
            method=meth,
            headers=headers,
            validate_certificate=True,
            deadline=55,
            payload=post_data
        )


if __name__ == '__main__':
    unittest2.main()
