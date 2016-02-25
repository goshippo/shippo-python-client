# Exceptions
class ShippoError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None):
        super(ShippoError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to support@goshippo.comom>')

        self.http_body = http_body

        self.http_status = http_status
        self.json_body = json_body


class APIError(ShippoError):
    pass


class APIConnectionError(ShippoError):
    pass


class AddressError(ShippoError):

    def __init__(self, message, param, code, http_body=None,
                 http_status=None, json_body=None):
        super(AddressError, self).__init__(message, http_body, http_status, json_body)
        self.param = param
        self.code = code


class InvalidRequestError(ShippoError):

    def __init__(self, message, param, http_body=None,
                 http_status=None, json_body=None):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body)
        self.param = param


class AuthenticationError(ShippoError):
    pass
