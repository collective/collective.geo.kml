import unittest
from collective.geo.kml.tests.base import TestCase


class TestColorConversion(TestCase):

    def test_colorconvert(self):
        from collective.geo.kml.utils import web2kmlcolor
        # convert standard web color
        self.assertEquals(web2kmlcolor('#ff00cc'), '3ccc00ff')
        # convert exadecimal color with alpha property
        self.assertEquals(web2kmlcolor('ff00cc3c'), '3ccc00ff')

        # convert null colors
        self.assertEquals(web2kmlcolor(None), '')
        self.assertEquals(web2kmlcolor(''), '')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestColorConversion))
    return suite
