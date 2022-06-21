import calendar
import datetime
import os
import platform
import socket
import ssl
import time
import urllib.parse
import warnings
import shippo

from shippo import error, http_client, util, certificate_blacklist
from shippo.version import VERSION


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _api_encode(data):
    for key, value in list(data.items()):
        key = key
        if value is None:
            continue
        elif hasattr(value, 'shippo_id'):
            yield (key, value.shippo_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for subvalue in value:
                yield ("%s[]" % (key,), subvalue)
        elif isinstance(value, dict):
            subdict = dict(('%s[%s]' % (key, subkey), subvalue) for
                           subkey, subvalue in list(value.items()))
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, value)


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urllib.parse.urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):

    _CERTIFICATE_VERIFIED = False

    def __init__(self, key=None, client=None):
        self.api_key = key

        from shippo.config import verify_ssl_certs, timeout_in_seconds

        self._client = client or http_client.new_default_http_client(
            verify_ssl_certs=verify_ssl_certs,
            timeout_in_seconds=timeout_in_seconds)

    def request(self, method, url, params=None):
        self._check_ssl_cert()\

        if params is not None and isinstance(params, dict):
            params = {('async' if k == 'asynchronous' else k): v for k, v in params.items()}

        rbody, rcode, my_api_key = self.request_raw(
            method.lower(), url, params)

        resp = self.interpret_response(rbody, rcode)
        return resp, my_api_key

    def handle_api_error(self, rbody, rcode, resp):

        if rcode in [400, 404]:
            raise error.InvalidRequestError(rbody, rcode, resp)
        elif rcode == 401:
            raise error.AuthenticationError(rbody, rcode, resp)
        else:
            raise error.APIError(rbody, rcode, resp)

    def request_raw(self, method, url, params=None):
        """
        Mechanism for issuing an API call
        """
        from shippo.config import api_version
        from shippo.config import app_name
        from shippo.config import app_version

        # app_name and app_version can be specified in shippo-python-client/shippo/config
        if app_name == '':
            app_name = 'PythonApp'

        if app_version == '':
            app_version = '1.0'

        if self.api_key:
            my_api_key = self.api_key
        else:
            from shippo.config import api_key
            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                'No API key provided. (HINT: set your API key using '
                '"shippo.config.api_key = shippo_test_d90f00698a0a8def0495fddb4212bb08051469d3"). You can generate API keys '
                'from the Shippo web interface.  See https://goshippo.com/api '
                'for details, or email support@goshippo.com if you have any '
                'questions.')

        token_type = 'ShippoToken'
        if my_api_key.startswith('oauth.'):
            token_type = 'Bearer'

        abs_url = '%s%s' % (shippo.config.api_base, url)

        if method == 'get' or method == 'delete':
            if params:
                encoded_params = urllib.parse.urlencode(
                    list(_api_encode(params or {})))
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post' or method == 'put':
            post_data = util.json.dumps(params)
        else:
            raise error.APIConnectionError(
                'Unrecognized HTTP method %r.  This may indicate a bug in the '
                'Shippo bindings.  Please contact support@goshippo.com for '
                'assistance.' % (method,))

        ua = {
            'bindings_version': VERSION,
            'lang': 'python',
            'publisher': 'shippo',
            'httplib': self._client.name,
        }
        for attr, func in [['lang_version', platform.python_version],
                           ['platform', platform.platform],
                           ['uname', lambda: ' '.join(platform.uname())]]:
            try:
                val = func()
            except Exception as e:
                val = "!! %s" % (e,)
            ua[attr] = val

        headers = {
            'Content-Type': 'application/json',
            'X-Shippo-Client-User-Agent': util.json.dumps(ua),
            'User-Agent': '%s/%s ShippoPythonSDK/%s' % (app_name, app_version, VERSION, ),
            'Authorization': '%s %s' % (token_type, my_api_key,)
        }

        if api_version is not None:
            headers['Shippo-API-Version'] = api_version

        rbody, rcode = self._client.request(
            method, abs_url, headers, post_data)
        util.logger.info(
            'API request to %s returned (response code, response body) of '
            '(%d, %r)',
            abs_url, rcode, rbody)
        return rbody, rcode, my_api_key

    def interpret_response(self, rbody, rcode):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
                if rbody == '':
                    rbody = '{"msg": "empty_response"}'
            resp = util.json.loads(rbody)                
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode)
        if not (200 <= rcode < 300):
            self.handle_api_error(rbody, rcode, resp)
        return resp

    def _check_ssl_cert(self):
        """Preflight the SSL certificate presented by the backend.

        This isn't 100% bulletproof, in that we're not actually validating the
        transport used to communicate with Shippo, merely that the first
        attempt to does not use a revoked certificate.

        Unfortunately the interface to OpenSSL doesn't make it easy to check
        the certificate before sending potentially sensitive data on the wire.
        This approach raises the bar for an attacker significantly."""

        from shippo.config import verify_ssl_certs

        if verify_ssl_certs and not self._CERTIFICATE_VERIFIED:
            uri = urllib.parse.urlparse(shippo.config.api_base)
            try:
                certificate = ssl.get_server_certificate(
                    (uri.hostname, uri.port or 443))
                der_cert = ssl.PEM_cert_to_DER_cert(certificate)
            except socket.error as e:
                raise error.APIConnectionError(e)
            except TypeError:
                # The Google App Engine development server blocks the C socket
                # module which causes a type error when using the SSL library
                if ('APPENGINE_RUNTIME' in os.environ and
                        'Dev' in os.environ.get('SERVER_SOFTWARE', '')):
                    self._CERTIFICATE_VERIFIED = True
                    warnings.warn(
                        'We were unable to verify Shippo\'s SSL certificate '
                        'due to a bug in the Google App Engine development '
                        'server. Please alert us immediately at '
                        'suppgoshippo.compo.com if this message appears in your '
                        'production logs.')
                    return
                else:
                    raise

            self._CERTIFICATE_VERIFIED = certificate_blacklist.verify(
                uri.hostname, der_cert)
