import os
import unittest2


def all():
    """
    Return all directories.

    Args:
    """
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest2.defaultTestLoader.discover(path)


def integration():
    """
    Return the default calibration.

    Args:
    """
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest2.defaultTestLoader.discover(
        os.path.join(path, "integration")
    )
