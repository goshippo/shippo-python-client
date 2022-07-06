import os
from typing import Optional

from shippo.version import VERSION


class Configuration:
    def __init__(self):
        self.sdk_version: str = VERSION
        self.api_base: str = os.environ.get('SHIPPO_API_BASE', 'https://api.goshippo.com/')
        self.api_key: str = os.environ.get('SHIPPO_API_KEY')
        self.api_version: str = os.environ.get('SHIPPO_API_VERSION', '2018-02-08')

        self.app_name: str = os.environ.get('APP_NAME', '')
        self.app_version: str = os.environ.get('APP_VERSION', '')

        self.sdk_name = 'ShippoPythonSDK'
        self.language = 'Python'

        self.verify_ssl_certs = True
        self.timeout_in_seconds: Optional[float] = None
        self.rates_req_timeout = float(os.environ.get('RATES_REQ_TIMEOUT', 20.0))

        # SETTINGS BELOW APPLY ONLY TO TESTS

        # Controls how much information is logged to stdout
        self.vcr_logging_level = os.environ.get('VCR_LOGGING_LEVEL', 'ERROR')

        # Switch to 'all' for re-recording all cassettes (to be used in CI so that all tests are run without mocks)
        self.vcr_record_mode = os.environ.get('VCR_RECORD_MODE', 'once')


config = Configuration()
