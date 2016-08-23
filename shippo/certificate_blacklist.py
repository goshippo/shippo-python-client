import hashlib
from shippo.error import APIError


BLACKLISTED_DIGESTS = {
}


def verify(hostname, certificate):
    """Verifies a PEM encoded certficate against a blacklist of known revoked
    fingerprints.

    returns True on success, raises RuntimeError on failure.
    """

    if hostname not in BLACKLISTED_DIGESTS:
        return True

    sha = hashlib.sha1()
    sha.update(certificate)
    fingerprint = sha.hexdigest()

    if fingerprint in BLACKLISTED_DIGESTS[hostname]:
        raise APIError("Invalid server certificate. You tried to "
                       "connect to a server that has a revoked "
                       "SSL certificate, which means we cannot "
                       "securely send data to that server. "
                       "Please email support@goshippo.comom if you "
                       "need help connecting to the correct API "
                       "server.")
    return True
