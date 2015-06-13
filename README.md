#Shippo Python API wrapper

Shippo is a shipping API that connects you with multiple shipping providers such as USPS, UPS, and Fedex through one interface and offers you great discounts.

Don't have an account? Sign up at https://goshippo.com/


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

### Full API documentation ###

* go to https://goshippo.com/docs/ for API documentation

* contact support@goshippo.com with any questions
