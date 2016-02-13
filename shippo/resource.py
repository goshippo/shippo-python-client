import urllib
import sys

from shippo import (
    api_requestor,
    api_version,
    error,
    util,
    rates_req_timeout
)


class ShippoObject(dict):

    def __init__(self, id=None, api_key=None, **params):
        super(ShippoObject, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()

        self._retrieve_params = params
        self._previous_metadata = None

        object.__setattr__(self, 'api_key', api_key)

        if id:
            self['object_id'] = id

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(ShippoObject, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError, err:
            raise AttributeError(*err.args)

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(ShippoObject, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(ShippoObject, self).__getitem__(k)
        except KeyError, err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Shippo's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(self.keys())))
            else:
                raise err

    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a ShippoObject. "
            "To unset a property, set it to None.")

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('object_id'), basestring):
            ident_parts.append('object_id=%s' % self.get('object_id'))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    @classmethod
    def construct_from(cls, values, api_key):
        instance = cls(values.get('object_id'), api_key)
        instance.refresh_from(values, api_key)
        return instance

    def refresh_from(self, values, api_key=None, partial=False):
        self.api_key = api_key or getattr(values, 'api_key', None)

        # Wipe old state before setting new.
        if partial:
            self._unsaved_values = (self._unsaved_values - set(values))
        else:
            removed = set(self.keys()) - set(values)
            self._transient_values = self._transient_values | removed
            self._unsaved_values = set()

            self.clear()

        self._transient_values = self._transient_values - set(values)

        for key, val in values.iteritems():
            super(ShippoObject, self).__setitem__(
                key, self.__class__.convert_to_shippo_object(val, api_key))

        self._previous_metadata = values.get('metadata')

    def request(self, method, url, params=None):
        if params is None:
            params = self._retrieve_params

        requestor = api_requestor.APIRequestor(self.api_key)
        response, api_key = requestor.request(method, url, params)
        return self.__class__.convert_to_shippo_object(response, api_key)

    def refresh(self):
        object_id = self.get('object_id')
        instance_url = self.__class__.instance_url(object_id)
        self.refresh_from(self.request('get', instance_url))
        return self

    @property
    def shippo_id(self):
        return self.id


class APIResource(ShippoObject):

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Address, Parcel)')
        return str(urllib.quote_plus(cls.__name__.lower()))

    @classmethod
    def class_path(cls):
        cls_name = cls.class_name()
        return "%ss" % cls_name

    @classmethod
    def class_url(cls):
        return 'v%s/%s' % (api_version, cls.class_path())

    @classmethod
    def instance_url(cls, object_id):
        if not object_id:
            raise error.InvalidRequestError(
                'Could not determine which URL to request: %s instance '
                'has invalid ID: %r' % (cls, object_id), 'object_id')
        object_id = util.utf8(object_id)
        base = cls.class_url()
        extn = urllib.quote_plus(object_id)
        return "%s/%s" % (base, extn)

    @classmethod
    def handle_request(cls, method, url, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        response, api_key = requestor.request(method, url, params)
        return cls.convert_to_shippo_object(response, api_key)

    @classmethod
    def convert_to_shippo_object(cls, resp, api_key):
        if isinstance(resp, list):
            return [cls.convert_to_shippo_object(i, api_key) for i in resp]
        elif isinstance(resp, dict) and not isinstance(resp, ShippoObject):
            resp = resp.copy()
            return cls.construct_from(resp, api_key)
        else:
            return resp


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, api_key=None, **params):
        return cls.handle_request('post', cls.class_url(), api_key, **params)


class ListableAPIResource(APIResource):

    @classmethod
    def all(cls, api_key=None, size=None, page=None, **params):
        """
        To retrieve a list of all the objects in a class. The size of page and
            the page number can be specified respectively cls.all(<size>,<page>)
            **NOTE: To specify a page number, the page size must also be provided
        """
        if page and not size:
            raise error.APIError('Must supply page size to specify page')

        url = cls.class_url()
        if size:
            extra = '?results=%s' % urllib.quote_plus(str(size))
            if page:
                extra = '%s&page=%s' % (extra, urllib.quote_plus(str(page)))
            url = '%s%s' % (url, extra)

        return cls.handle_request('get', url, api_key, **params)


class FetchableAPIResource(APIResource):

    @classmethod
    def retrieve(cls, object_id, api_key=None, **params):
        url = cls.instance_url(object_id)
        return cls.handle_request('get', url, api_key, **params)


class UpdateableAPIResource(APIResource):

    @classmethod
    def update(cls, object_id, api_key=None, **params):
        url = cls.instance_url(object_id)
        return cls.handle_request('put', url, api_key, **params)


# ---- API objects ----

class Address(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def validate(cls, object_id, api_key=None, **params):
        url = '%s/%s' % (cls.instance_url(object_id), 'validate')
        return cls.handle_request('get', url, api_key, **params)

    @classmethod
    def class_path(cls):
        return "addresses"


class CustomsItem(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def class_path(cls):
        return "customs/items"


class CustomsDeclaration(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def class_path(cls):
        return "customs/declarations"


class Parcel(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    pass


class Manifest(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
     Manifests are close-outs of shipping labels of a certain day. Some carriers
        require Manifests to properly process the shipments
    """


class Refund(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
        Refunds are reimbursements for successfully created but unused Transaction.
    """


class Shipment(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
        The heart of the Shippo API, a Shipment is made up of "to" and "from" Addresses
        and the Parcel to be shipped. Shipments can be created, retrieved and listed.
    """

    def get_rates(self, currency=None, **params):
        cls = self.__class__
        url = '%s/%s' % (cls.instance_url(self.get('object_id')), 'rates')
        if currency:
            url = '%s/%s' % (url, urllib.quote_plus(currency))
        return Rate.handle_request('get', url, self.get('api_key'), **params)


class Transaction(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
        A Transaction is the purchase of a Shipment Label for a given Shipment Rate.
        Transactions can be as simple as posting a Rate ID.
    """

    @classmethod
    def create(cls, api_key=None, **params):
        """
            Creates a new transaction object, given a valid rate ID.
            Takes the parameters as a dictionary instead of key word arguments.
        """
        return cls.handle_request('post', cls.class_url(), api_key, **params)


class Rate(ListableAPIResource, FetchableAPIResource):
    """
     Each valid Shipment object will automatically trigger the calculation of all available
     Rates. Depending on your Addresses and Parcel, there may be none, one or multiple Rates
    """


class CarrierAccount(CreateableAPIResource, ListableAPIResource, FetchableAPIResource, UpdateableAPIResource):

    @classmethod
    def class_path(cls):
        return "carrier_accounts"
