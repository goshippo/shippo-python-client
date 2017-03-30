import urllib
import sys
import time
import warnings

from shippo import api_requestor, error, util, rates_req_timeout

warnings.filterwarnings('always', category=DeprecationWarning, module='shippo')


def convert_to_shippo_object(resp, api_key):
    if isinstance(resp, list):
        return [convert_to_shippo_object(i, api_key) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, ShippoObject):
        resp = resp.copy()
        return ShippoObject.construct_from(resp, api_key)
    else:
        return resp


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

        for k, v in values.iteritems():
            super(ShippoObject, self).__setitem__(
                k, convert_to_shippo_object(v, api_key))

        self._previous_metadata = values.get('metadata')

    def request(self, method, url, params=None):
        if params is None:
            params = self._retrieve_params

        requestor = api_requestor.APIRequestor(self.api_key)
        response, api_key = requestor.request(method, url, params)

        return convert_to_shippo_object(response, api_key)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('object_id'), basestring):
            ident_parts.append('object_id=%s' % (self.get('object_id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    @property
    def shippo_id(self):
        return self.id


class APIResource(ShippoObject):

    def refresh(self):
        self.refresh_from(self.request('get', self.instance_url()))
        return self

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Address, Parcel)')
        return str(urllib.quote_plus(cls.__name__.lower()))

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/v1/%ss" % (cls_name,)

    def instance_url(self):
        object_id = self.get('object_id')
        if not object_id:
            raise error.InvalidRequestError(
                'Could not determine which URL to request: %s instance '
                'has invalid ID: %r' % (type(self).__name__, object_id), 'object_id')
        object_id = util.utf8(object_id)
        base = self.class_url()
        extn = urllib.quote_plus(object_id)
        return "%s/%s" % (base, extn)


class CreateableAPIResource(APIResource):

    @classmethod
    def create(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request('post', url, params)
        return convert_to_shippo_object(response, api_key)


class ListableAPIResource(APIResource):

    @classmethod
    def all(cls, api_key=None, size=None, page=None, **params):
        """
        To retrieve a list of all the objects in a class. The size of page and
            the page number can be specified respectively cls.all(<size>,<page>)
            **NOTE: To specify a page number, the page size must also be provided
        """
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        if size:
            url = url+'?results='+urllib.quote_plus(str(size))
        if page:
            url = url+'&page='+urllib.quote_plus(str(page))
        response, api_key = requestor.request('get', url, params)
        return convert_to_shippo_object(response, api_key)


class FetchableAPIResource(APIResource):

    @classmethod
    def retrieve(cls, object_id, api_key=None):
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn
        response, api_key = requestor.request('get', url)
        return convert_to_shippo_object(response, api_key)


class UpdateableAPIResource(APIResource):

    @classmethod
    def update(cls, object_id, api_key=None, **params):
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn
        response, api_key = requestor.request('put', url, params)
        return convert_to_shippo_object(response, api_key)


# ---- API objects ----

class Address(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def validate(cls, object_id, api_key=None):
        extn = urllib.quote_plus(object_id)
        url = cls.class_url() + extn + '/validate'
        requestor = api_requestor.APIRequestor(api_key)
        response, api_key = requestor.request('get', url)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ses/" % (cls_name,)


class CustomsItem(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def class_url(cls):
        return "v1/customs/items/"


class CustomsDeclaration(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def class_url(cls):
        return "v1/customs/declarations/"


class Parcel(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class Manifest(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
     Manifests are close-outs of shipping labels of a certain day. Some carriers
        require Manifests to properly process the shipments
    """

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class Refund(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
        Refunds are reimbursements for successfully created but unused Transaction.
    """

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class Shipment(CreateableAPIResource, ListableAPIResource, FetchableAPIResource):
    """
        The heart of the Shippo API, a Shipment is made up of "to" and "from" Addresses
        and the Parcel to be shipped. Shipments can be created, retrieved and listed.
    """

    @classmethod
    def get_rates(cls, object_id, async=False, api_key=None, currency=None, **params):
        """
            Given a valid shipment object_id, all possible rates are calculated and returned.
        """
        if 'sync' in params:
            warnings.warn('The `sync` parameter is deprecated. '
                          'Use `async` while creating a shipment instead.', DeprecationWarning)
            # will be removed in the next major version
            if params.get('sync') is not None:
                async = not params['sync']

        if not async:
            timeout = time.time() + rates_req_timeout
            while cls.retrieve(object_id, api_key=api_key).status in ("QUEUED", "WAITING") and time.time() < timeout:
                continue

        shipment_id = urllib.quote_plus(object_id)
        url = cls.class_url() + shipment_id + '/rates/'
        if currency:
            url = url + '' + urllib.quote_plus(currency)
        requestor = api_requestor.APIRequestor(api_key)
        response, api_key = requestor.request('get', url)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


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
        # will be removed in the next major version
        if 'sync' in params:
            warnings.warn('The `sync` parameter is deprecated. '
                          'Use `async` instead.', DeprecationWarning)
            params['async'] = False if params.get('sync') is None else (not params['sync'])

        return super(Transaction, cls).create(api_key, **params)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class Rate(ListableAPIResource, FetchableAPIResource):
    """
     Each valid Shipment object will automatically trigger the calculation of all available
     Rates. Depending on your Addresses and Parcel, there may be none, one or multiple Rates
    """

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class CarrierAccount(CreateableAPIResource, ListableAPIResource, FetchableAPIResource, UpdateableAPIResource):

    @classmethod
    def class_url(cls):
        return "v1/carrier_accounts/"


class Track(CreateableAPIResource):
    """
    A Track object gives you the current shipping state of a package not tendered through Shippo
    given a carrier and respective tracking number. It also allows you to register a webhook to
    a carrier + tracking number pair in order to receive live updates.

    Tracking packages tendered through Shippo can be done through the Transaction object
    """
    @classmethod
    def get_status(cls, carrier_token, tracking_number, api_key=None):
        """
        A custom get method for tracking based on carrier and tracking number
        Written because the endpoint for tracking is different from our standard endpoint
        
        Arguments:
            carrier_token (str) -- name of the carrier of the shipment to track
                                    see https://goshippo.com/docs/reference#carriers
            tracking_number (str) -- tracking number to track

        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        carrier_token = urllib.quote_plus(util.utf8(carrier_token))
        tracking_number = urllib.quote_plus(util.utf8(tracking_number))
        tn = urllib.quote_plus(tracking_number)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + carrier_token + '/' + tracking_number
        response, api_key = requestor.request('get', url)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def create(cls, api_key=None, **params):
        """
        Creates a webhook to keep track of the shipping status of a specific package
                
        Arguments:
            **params
                carrier (str) -- name of the carrier of the shipment to track
                                  see https://goshippo.com/docs/reference#carriers
                tracking_number (str) -- tracking number to track
                metadata (str) -- A string of up to 100 characters that can be filled with any 
                                   additional information you want to attach to the object
        
        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        return super(Track, cls).create(api_key, **params)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ss/" % (cls_name,)


class Batch(CreateableAPIResource, FetchableAPIResource):
    """
    A Batch bundles together large amounts of shipments, up to 10,000
    """
    @classmethod
    def retrieve(cls, object_id, api_key=None, **params):
        """
        Retrieve a batch, customized to allow the addition of url parameters
        
        Arguments:
            object_id (str) -- the batch object id
            **params
                page (int as str) -- pagination
                object_results (str) -- valid options are:
                                            "creation_failed"
                                            "creation_succeeded"
                                            "purchase_succeeded"
                                            "purchase_failed"
        
        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        glue = '?'
        for key in params:
            extn += glue + key + '=' + str(params[key])
            if glue == '?':
                glue = '&'
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn
        response, api_key = requestor.request('get', url)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def add(cls, object_id, shipments_to_add, api_key=None):
        """
        Add shipments to a batch
        
        Arguments:
            object_id (str) -- the batch object id
            shipments_to_add (list of dict) -- list of shipments to add, must be in the format
                [{'shipment': <shipment 1 object id>}, {'shipment': <shipment 2 object id>}, ...]

        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn + '/add_shipments'
        response, api_key = requestor.request('post', url, shipments_to_add)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def remove(cls, object_id, shipments_to_remove, api_key=None):
        """
        Remove shipments from a batch
        
        Arguments:
            object_id (str) -- the batch object id
            shipments_to_remove (list of str) -- list of shipments to remove, must be in the format
                [<shipment 1 object id>, <shipment 2 object id>, ...]
        
        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn + '/remove_shipments'
        response, api_key = requestor.request('post', url, shipments_to_remove)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def purchase(cls, object_id, api_key=None):
        """
        Purchase batch of shipments
        
        Arguments:
            object_id (str) -- the batch object id
        
        Keyword Arguments:
            api_key (str) -- an api key, if not specified here it will default to the key
                             set in your environment var or by shippo.api_key = "..."

        Returns:
            (ShippoObject) -- The server response
        """
        object_id = util.utf8(object_id)
        extn = urllib.quote_plus(object_id)
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + extn + '/purchase'
        response, api_key = requestor.request('post', url)
        return convert_to_shippo_object(response, api_key)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "v1/%ses/" % (cls_name,)
