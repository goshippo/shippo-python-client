import os
import unittest


def all():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(path)


def integration():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(
        os.path.join(path, "integration")
    )
