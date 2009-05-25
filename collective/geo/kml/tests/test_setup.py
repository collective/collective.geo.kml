import unittest
from collective.geo.kml.tests.base import KmlTestCase
from Products.CMFPlone.utils import getToolByName

class TestSetup(KmlTestCase):
    pass
    #def test_portal_skins(self):
        #skins = getToolByName(self.portal, 'portal_skins')
        #layer = skins.getSkinPath('Plone Default')
        #self.failUnless('geo_openlayers' in layer)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
