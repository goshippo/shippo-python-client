import warnings
import unittest2

from mock import Mock
import shippo

from shippo.test.helper import ShippoUnitTestCase

VALID_API_METHODS = ('get', 'post', 'delete')


class HttpClientTests(ShippoUnitTestCase):

    def setUp(self):
        """
        Set the default filters.

        Args:
            self: (todo): write your description
        """
        super(HttpClientTests, self).setUp()

        self.original_filters = warnings.filters[:]
        warnings.simplefilter('ignore')

    def tearDown(self):
        """
        Tear down the session.

        Args:
            self: (todo): write your description
        """
        warnings.filters = self.original_filters

        super(HttpClientTests, self).tearDown()

    def check_default(self, none_libs, expected):
        """
        Check the default libs for the default libs.

        Args:
            self: (todo): write your description
            none_libs: (todo): write your description
            expected: (list): write your description
        """
        for lib in none_libs:
            setattr(shippo.http_client, lib, None)

        inst = shippo.http_client.new_default_http_client()

        self.assertTrue(isinstance(inst, expected))

    def test_new_default_http_client_urlfetch(self):
        """
        Create a new http client.

        Args:
            self: (todo): write your description
        """
        self.check_default((), shippo.http_client.UrlFetchClient)

    def test_new_default_http_client_requests(self):
        """
        Creates a new http client.

        Args:
            self: (todo): write your description
        """
        self.check_default(('urlfetch',), shippo.http_client.RequestsClient)


class ClientTestBase():

    @property
    def request_mock(self):
        """
        Returns a request.

        Args:
            self: (todo): write your description
        """
        return self.request_mocks[self.request_client.name]

    @property
    def valid_url(self, path='/v1/echo'):
        """
        Return the url.

        Args:
            self: (todo): write your description
            path: (str): write your description
        """
        return 'https://api.goshippo.com%s' % (path,)

    def make_request(self, method, url, headers, post_data):
        """
        Make a request to the http post request.

        Args:
            self: (todo): write your description
            method: (str): write your description
            url: (str): write your description
            headers: (dict): write your description
            post_data: (dict): write your description
        """
        client = self.request_client(verify_ssl_certs=True)
        return client.request(method, url, headers, post_data)

    def mock_response(self, body, code):
        """
        Mock a flask response.

        Args:
            self: (todo): write your description
            body: (todo): write your description
            code: (str): write your description
        """
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def mock_error(self, error):
        """
        Makes an error.

        Args:
            self: (todo): write your description
            error: (todo): write your description
        """
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def check_call(self, meth, abs_url, headers, params):
        """
        Make a call.

        Args:
            self: (todo): write your description
            meth: (str): write your description
            abs_url: (str): write your description
            headers: (str): write your description
            params: (dict): write your description
        """
        raise NotImplementedError(
            'You must implement this in your test subclass')

    def test_request(self):
        """
        Perform the test request.

        Args:
            self: (todo): write your description
        """
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
        """
        Test if the http request.

        Args:
            self: (todo): write your description
        """
        self.mock_error(self.request_mock)
        self.assertRaises(shippo.error.APIConnectionError,
                          self.make_request,
                          'get', self.valid_url, {}, None)


class RequestsVerify(object):

    def __eq__(self, other):
        """
        Determine if two values are equal.

        Args:
            self: (todo): write your description
            other: (todo): write your description
        """
        return other and other.endswith('shippo/data/ca-certificates.crt')


class RequestsClientTests(ShippoUnitTestCase, ClientTestBase):
    request_client = shippo.http_client.RequestsClient

    def mock_response(self, mock, body, code):
        """
        Makes a mock response.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
            body: (todo): write your description
            code: (str): write your description
        """
        result = Mock()
        result.content = body
        result.status_code = code

        mock.request = Mock(return_value=result)

    def mock_error(self, mock):
        """
        Makes a mock error.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
        """
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, mock, meth, url, post_data, headers):
        """
        Perform a call.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
            meth: (str): write your description
            url: (str): write your description
            post_data: (dict): write your description
            headers: (str): write your description
        """
        mock.request.assert_called_with(meth, url,
                                        headers=headers,
                                        data=post_data,
                                        verify=RequestsVerify(),
                                        timeout=80)


class UrlFetchClientTests(ShippoUnitTestCase, ClientTestBase):
    request_client = shippo.http_client.UrlFetchClient

    def mock_response(self, mock, body, code):
        """
        Makes a response.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
            body: (todo): write your description
            code: (str): write your description
        """
        result = Mock()
        result.content = body
        result.status_code = code

        mock.fetch = Mock(return_value=result)

    def mock_error(self, mock):
        """
        Mock a mock error.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
        """
        mock.Error = mock.InvalidURLError = Exception
        mock.fetch.side_effect = mock.InvalidURLError()

    def check_call(self, mock, meth, url, post_data, headers):
        """
        : paramiko call is valid.

        Args:
            self: (todo): write your description
            mock: (todo): write your description
            meth: (str): write your description
            url: (str): write your description
            post_data: (dict): write your description
            headers: (str): write your description
        """
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
