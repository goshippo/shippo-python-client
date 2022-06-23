import logging

from shippo.config import config

logger = logging.getLogger('shippo')

logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(config.vcr_logging_level)


__all__ = ['json']

try:
    import json
except ImportError:
    json = None

if not (json and hasattr(json, 'loads')):
    try:
        import simplejson as json
    except ImportError:
        if not json:
            raise ImportError(
                "Shippo requires a JSON library, such as simplejson. "
                "HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' or "
                "contact support@goshippo.com with questions.")
        else:
            raise ImportError(
                "Shippo requires a JSON library with the same interface as "
                "the Python 2.6 'json' library.  You appear to have a 'json' "
                "library with a different interface.  Please install "
                "the simplejson library.  HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' "
                "contact support@goshippo.com with questions.")
