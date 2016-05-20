#Shippo API Python wrapper

Shippo is a shipping API that connects you with multiple shipping carriers (such as USPS, UPS, DHL, Canada Post, Australia Post, UberRUSH and many [others](https://goshippo.com/shipping-carriers/)) through one interface.

Our API provides in depth support of carrier functionality. Here are just some of the features we support for USPS, FedEx and UPS via the API.

For most major carriers (USPS, UPS, FedEx and most others) our API supports:

* Shipping rates & labels
* Tracking
	
* For USPS, the API additionally supports:
	* US Address validation
	* Scan forms
	* Additional services: signature, certified mail, delivery confirmation, and others

* For FedEx, the API additionally supports:
	* Signature and adult signature confirmation
	* FedEx Smartpost

* For UPS, the API additionally supports:
	* Signature and adult signature confirmation
	* UPS Mail Innovations
	* UPS SurePost

The complete list of carrier supported features is [here](https://goshippo.com/shipping-api/carriers).

###About Shippo
Connect with multiple different carriers, get discounted shipping labels, track parcels, and much more with just one integration. You can use your own carrier accounts or take advantage of our deeply discounted rates. Using Shippo makes it easy to deal with multiple carrier integrations,  rate shopping, tracking and other parts of the shipping workflow. We provide the API and dashboard for all your shipping needs.

The API is free to use. You only pay when you print a live label from a carrier.  Use test labels during development to avoid all fees.

You do need a Shippo account to use our API. Don't have an account? Sign up at [https://goshippo.com/](https://goshippo.com/).

### How do I get set up? ###

####To install from the source file:

```
#!shell
python setup.py install
```

or pip (https://pip.pypa.io/en/latest/index.html):
```
#!shell
sudo pip install shippo
``` 

#### To test:

Add your `<API-KEY>` in `/test/helper.py`

Run the test with the following command:

```
#!shell
python setup.py test --test-suite=shippo
```


#### Dependencies:

##### requests & mock

```
#!shell
sudo easy_install requests
sudo easy_install mock
``` 

#### Using the API:

```
import shippo
shippo.api_key = "<API-KEY>"

address1 = shippo.Address.create(
    object_purpose='PURCHASE',
    name='John Smith',
    street1='6512 Greene Rd.',
    street2='',
    company='Initech',
    phone='+1 234 346 7333',
    city='Woodridge',
    state='IL',
    zip='60517',
    country='US',
    email='user@gmail.com',
    metadata='Customer ID 123456'
)

print 'Success with Address 1 : %r' % (address1, )
```

and you will have created an address. 

Explore example.py for more examples on using the python wrapper.

## Documentation

Please see [https://goshippo.com/shipping-api/](https://goshippo.com/shipping-api/) for up-to-date documentation.
