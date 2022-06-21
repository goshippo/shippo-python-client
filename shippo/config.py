import os

# Configurable variables
api_key = os.environ.get('SHIPPO_API_KEY')
api_base = os.environ.get('SHIPPO_API_BASE', 'https://api.goshippo.com/')
api_version = os.environ.get('SHIPPO_API_VERSION', '2018-02-08')
verify_ssl_certs = True
rates_req_timeout = 20.0
timeout_in_seconds = None
app_name = 'PythonApp'
app_version = '1.0'
vcr_logging_level = 'ERROR'