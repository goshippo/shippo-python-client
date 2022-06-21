import os

# Configurable variables
api_key = os.environ.get('SHIPPO_API_KEY', 'shippo_test_cf1b6d0655e59fc6316880580765066038ef20d8')
api_base = os.environ.get('SHIPPO_API_BASE', 'https://api.goshippo.com/')
api_version = os.environ.get('SHIPPO_API_VERSION', '2018-02-08')
verify_ssl_certs = True
rates_req_timeout = 20.0
vcr_logging_level = 'ERROR'
