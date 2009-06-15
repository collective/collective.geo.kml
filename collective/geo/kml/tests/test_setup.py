import unittest
from collective.geo.kml.tests.base import KmlTestCase

class TestSetup(KmlTestCase):
    pass

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
