import unittest2 as unittest
from ..testing import CGEO_KML


class TestSetup(unittest.TestCase):
    layer = CGEO_KML

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
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
