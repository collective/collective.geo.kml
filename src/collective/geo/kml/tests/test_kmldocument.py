import unittest2 as unittest
from ..testing import CGEO_KML_INTEGRATION


class TestKMLDocument(unittest.TestCase):
    layer = CGEO_KML_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_lead_image_render(self):
        from collective.geo.kml.browser import kmldocument
        from plone.namedfile.file import NamedBlobImage, NamedImage
        from plone.namedfile.tests.test_blobfile import registerUtilities
        from mock import Mock

        # get NamedBlobImage/NamedImage to work in this test
        registerUtilities()

        # so we don't need collective.contentleadimage for the test
        kmldocument.HAS_LEADIMAGE = True

        # we could use ATImage, but since that is deprecated, we just mock it
        class ATImage(object):
            def get_size(self, obj):
                return 1

            def tag(self, obj, scale, css_class):
                return '<img>'

        placemark = kmldocument.Placemark(self.portal, self.request)
        placemark.context.getField = Mock(return_value=ATImage())

        self.assertEqual(placemark.lead_image(), '<img>')

        # now let's try with NamedBlobImage and NamedImage
        placemark.context.getField = Mock(return_value=NamedImage())
        self.assertEqual(placemark.lead_image(), None)

        placemark.context.getField = Mock(return_value=NamedBlobImage())
        self.assertEqual(placemark.lead_image(), None)

        # or anything else really
        placemark.context.getField = Mock(return_value=object())
        self.assertEqual(placemark.lead_image(), None)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestKMLDocument))
    return suite
