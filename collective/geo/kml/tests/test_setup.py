import unittest
from collective.geo.kml.tests.base import TestCase
# from Products.CMFCore.utils import getToolByName


class TestSetup(TestCase):
    pass
    # def afterSetUp(self):
    #     self.cat = getToolByName(self.portal, 'portal_catalog')
    # 
    # def test_catalog_metadata(self):
    #     self.failUnless('zgeo_geometry' in self.cat.schema(), self.cat.schema())

    def test_colorconvert(self):
        from collective.geo.kml.utils import web2kmlcolor
        self.assertEquals(web2kmlcolor('#FF00CC'), 'FFCC00FF')

        self.assertEquals(web2kmlcolor(None), '')
        self.assertEquals(web2kmlcolor(''), '')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
