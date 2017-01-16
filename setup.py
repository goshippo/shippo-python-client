import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = ['requests >= 1.0.0', 'six']

# Don't import shippo module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shippo'))
from version import VERSION

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')

setup(
    name='shippo',
    cmdclass={'build_py': build_py},
    version=VERSION,
    description='Shipping API Python library (USPS, FedEx, UPS and more)',
    author='Shippo',
    author_email='support@goshippo.com',
    url='https://goshippo.com/',
    packages=['shippo', 'shippo.test', 'shippo.test.integration'],
    package_data={'shippo': ['../VERSION']},
    install_requires=install_requires,
    test_suite='shippo.test.all',
    tests_require=['unittest2', 'mock', 'vcrpy'],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
