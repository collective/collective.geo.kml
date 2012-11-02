import unittest2 as unittest
import doctest

from plone.testing import layered
from ..testing import CGEO_KML_FUNCTIONAL


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([

        layered(
            doctest.DocFileSuite(
                'README.txt',
                package='collective.geo.kml',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                            doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        layered(
            doctest.DocFileSuite(
                'browser/kmlopenlayersview.txt',
                package='collective.geo.kml',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        layered(
            doctest.DocFileSuite(
                'kml-docs.txt',
                package='collective.geo.kml.tests',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        layered(
            doctest.DocFileSuite(
                'folder-kml.txt',
                package='collective.geo.kml.tests',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
