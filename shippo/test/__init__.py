import os
import unittest


def all():
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        return unittest.defaultTestLoader.discover(path)
    except Exception as err:
        import pdb; pdb.set_trace()
        print err


def integration():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(
        os.path.join(path, "integration")
    )
