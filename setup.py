import os
import sys
import warnings
from setuptools import setup


version_contents = {}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "shippo", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setup(
    name='shippo',
    version=version_contents['VERSION'],
    description='Shipping API Python library (USPS, FedEx, UPS and more)',
    author='Shippo',
    author_email='support@goshippo.com',
    url='https://goshippo.com/',
    packages=['shippo', 'shippo.test', 'shippo.test.integration'],
    package_data={'shippo': ['../VERSION']},
    install_requires=[
        'requests == 2.21.0',
        'simplejson == 3.16.0',
    ],
    test_suite='shippo.test.all',
    tests_require=['unittest2', 'mock', 'vcrpy'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
