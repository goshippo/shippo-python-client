# Shippo Python Wrapper #

This document helps you setup and get started with using the Shippo API in your python project.


### How do I get set up? ###

* To install from the source file:

```
#!shell

 python setup.py install

```
   
* To Install from pip or easy_install:

easy_install (https://pythonhosted.org/setuptools/easy_install.html):

```
#!shell

    sudo easy_install shippo
```

or pip (https://pip.pypa.io/en/latest/index.html):
```
#!shell

    sudo pip install shippo
``` 

* Dependencies :

- requests & mock
```
#!shell
   sudo easy_install requests
   sudo easy_install mock
``` 

* Using the API :

- Start a new python file, import the shippo package, and enter your shippo credentials
```
#!python

import shippo
shippo.auth = ('username', 'password')

```
- Then use the shippo API to create Addresses, Shipments, Rates and much more. Here is a code snippet for creating an address:
```
#!python
address1 = shippo.Address.create(
    object_purpose='PURCHASE',
    name='John Smith',
    street1='Greene Rd.',
    street2='',
    company='Initech',
    street_no='6512',
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
