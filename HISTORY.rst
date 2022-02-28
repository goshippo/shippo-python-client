Release History
---------------

2.1.2 (2022-02-28)
2.1.1 (2022-02-28) [--removed](https://pypi.org/manage/project/shippo/history/) 

**Dependency Version Bumps**

- Allow requests version to be higher (2.27.1)

Release History
---------------

2.1.0 (2022-01-18)

**New features**

- Added support for Pickup and Order Objects
- Converted testing to CircleCi

Release History
---------------

2.0.2 (2020-11-05)

**Dependency Version Bumps**

- Allow simplejson version to be higher (3.17.2)
- Allow requests version to be higher (2.24.0)

Release History
---------------

2.0.1 (2020-9-21)

**Improvements**

- Add Webhook Class
- Add multi-piece shipment & webhook examples

Release History
---------------

2.0.0 (2020-01-10)

**Behavioural Changes**

- Update default API version to 2018-02-08. For more information on versioning and upgrading your version, please refer to https://goshippo.com/docs/versioning

2.0.0rc1 (2019-05-06)
+++++++++++++++++++

**Behavioural Changes**

- Drop support for Python < 3.5
- Drop `async` and `sync` parameters in favour of `asynchronous`
- Move configurations to `shippo.config`

1.5.1 (2017-04-10)
+++++++++++++++++++

**Behavioural Changes**

- Remove unnecessary email fields and amend parcel fields to match the new version

1.5.0 (2017-03-29)
+++++++++++++++++++

**Behavioural Changes**

- The client now only supports the most recent version of the Shippo API (2017-03-29). For more information on versioning and upgrading your version, please refer to https://goshippo.com/docs/versioning

1.4.0 (2017-01-19)
+++++++++++++++++++

**Improvements**

- SSL cert verification is now enabled by default

1.3.0 (2017-01-18)
+++++++++++++++++++

**New features**

- Added support for Track and Batch Objects

1.2.4 (2016-10-11)
+++++++++++++++++++

**Bugfixes**

- Change the API version header name

1.2.3 (2016-09-27)
+++++++++++++++++++

**Minor Improvements**

- Fix relative imports for Python 3

1.2.2 (2016-08-1)
+++++++++++++++++++

**Minor Improvements**

- Only show DeprecationWarning for shippo package.

1.2.1 (2016-06-13)
+++++++++++++++++++

**Bugfixes**

- add version to shippo

1.2.0 (2016-06-13)
+++++++++++++++++++

**Improvements**

- Removed polling for shipments and transactions calls
- Fixed and added tests

**Behavioural Changes**

- [WARNING] Changed keyword for creating shipments and transactions synchronously from `sync=True` to `async=False`

**Minor Improvements**

- Added fixtures to our tests using vcr
- Added Travis-CI
- Added badges to the README
- Bumped unittest version

1.1.1 (2015-11-12)
+++++++++++++++++++


1.1.0 (2015-06-12)
+++++++++++++++++++
