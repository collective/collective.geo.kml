import unittest
from collective.geo.kml.tests.base import TestCase


class TestColorConversion(TestCase):

    def test_colorconvert(self):
        from collective.geo.kml.utils import web2kmlcolor
        # convert standard web color
        self.assertEquals(web2kmlcolor('#FF00CC'), '3CCC00FF')
        # convert exadecimal color with alpha property
        self.assertEquals(web2kmlcolor('FF00CC3C'), '3CCC00FF')

        # convert null colors
        self.assertEquals(web2kmlcolor(None), '')
        self.assertEquals(web2kmlcolor(''), '')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestColorConversion))
    return suite
