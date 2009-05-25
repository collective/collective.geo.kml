import unittest
from zope.testing import doctest, doctestunit
from collective.geo.kml.tests import base

import collective.geo.kml.geokmlconfig
import zope.component

from zope.component import provideUtility
from collective.geo.kml import geokmlconfig 
from collective.geo.kml import interfaces

def setUp(test):
    # registrazione della mia utility .. componentregistry.xml
    provideUtility(
              geokmlconfig.GeoKmlSettings, 
              provides = interfaces.IGeoKmlSettings
              )


def tearDown(test):
    """This is the companion to setUp - it can be used to clean up the 
    test environment after each test.
    """
    
def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.kml.geokmlconfig,
                     setUp=setUp, 
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
