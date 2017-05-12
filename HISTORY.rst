Release History
---------------
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
