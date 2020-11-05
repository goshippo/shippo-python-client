# Exceptions
class ShippoError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None):
        """
        Initialize a http status message.

        Args:
            self: (todo): write your description
            message: (str): write your description
            http_body: (str): write your description
            http_status: (str): write your description
            json_body: (str): write your description
        """
        super(ShippoError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to support@goshippo.com>')

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
        """
        Initialize http status code.

        Args:
            self: (todo): write your description
            message: (str): write your description
            param: (todo): write your description
            code: (int): write your description
            http_body: (todo): write your description
            http_status: (str): write your description
            json_body: (str): write your description
        """
        super(AddressError, self).__init__(
            message, http_body, http_status, json_body)
        self.param = param
        self.code = code


class InvalidRequestError(ShippoError):

    def __init__(self, message, param, http_body=None,
                 http_status=None, json_body=None):
        """
        Initialize a message.

        Args:
            self: (todo): write your description
            message: (str): write your description
            param: (todo): write your description
            http_body: (todo): write your description
            http_status: (str): write your description
            json_body: (str): write your description
        """
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body)
        self.param = param


class AuthenticationError(ShippoError):
    pass
