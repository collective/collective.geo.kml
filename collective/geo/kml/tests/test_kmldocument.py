import unittest
from zope.testing import doctest

import collective.geo.kml.browser.kml

def setUp(test):
    pass


def tearDown(test):
    """This is the companion to setUp - it can be used to clean up the
    test environment after each test.
    """

def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.kml.browser.kml,
                     setUp=setUp,
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
