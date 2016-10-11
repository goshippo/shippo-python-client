import calendar
import datetime
import os
import platform
import socket
import ssl
import time
import urllib
import urlparse
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
    for key, value in data.iteritems():
        key = util.utf8(key)
        if value is None:
            continue
        elif hasattr(value, 'shippo_id'):
            yield (key, value.shippo_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for subvalue in value:
                yield ("%s[]" % (key,), util.utf8(subvalue))
        elif isinstance(value, dict):
            subdict = dict(('%s[%s]' % (key, subkey), subvalue) for
                           subkey, subvalue in value.iteritems())
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlparse.urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):

    _CERTIFICATE_VERIFIED = False

    def __init__(self, key=None, client=None):
        self.api_key = key

        from shippo import verify_ssl_certs

        self._client = client or http_client.new_default_http_client(
            verify_ssl_certs=verify_ssl_certs)

    def request(self, method, url, params=None):
        self._check_ssl_cert()
        rbody, rcode, my_api_key = self.request_raw(
            method.lower(), url, params)

        resp = self.interpret_response(rbody, rcode)
        return resp, my_api_key

    def handle_api_error(self, rbody, rcode, resp):

        if rcode in [400, 404]:
            raise error.InvalidRequestError(rbody, rcode, resp)
        elif rcode == 401:
            raise error.AuthenticationError(rbody, rcode, resp)
        elif rcode == 402:
            raise error.CardError(rbody, rcode, resp)
        else:
            raise error.APIError(rbody, rcode, resp)

    def request_raw(self, method, url, params=None):
        """
        Mechanism for issuing an API call
        """
        from shippo import api_version

        if self.api_key:
            my_api_key = self.api_key
        else:
            from shippo import api_key
            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                'No API key provided. (HINT: set your API key using '
                '"shippo.api_key = <API-KEY>"). You can generate API keys '
                'from the Shippo web interface.  See https://goshippo.com/api '
                'for details, or email support@goshippo.comom if you have any '
                'questions.')

        abs_url = '%s%s' % (shippo.api_base, url)

        if method == 'get' or method == 'delete':
            if params:
                encoded_params = urllib.urlencode(list(_api_encode(params or {})))
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post' or method == 'put':
            post_data = util.json.dumps(params)
        else:
            raise error.APIConnectionError(
                'Unrecognized HTTP method %r.  This may indicate a bug in the '
                'Shippo bindings.  Please contact support@goshippo.com.com for '
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
            except Exception, e:
                val = "!! %s" % (e,)
            ua[attr] = val

        headers = {
            'Content-Type': 'application/json',
            'X-Shippo-Client-User-Agent': util.json.dumps(ua),
            'User-Agent': 'Shippo/v1 PythonBindings/%s' % (VERSION, ),
            'Authorization': 'ShippoToken %s' % (my_api_key,)
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

        from shippo import verify_ssl_certs

        if verify_ssl_certs and not self._CERTIFICATE_VERIFIED:
            uri = urlparse.urlparse(shippo.api_base)
            try:
                certificate = ssl.get_server_certificate(
                    (uri.hostname, uri.port or 443))
                der_cert = ssl.PEM_cert_to_DER_cert(certificate)
            except socket.error, e:
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
