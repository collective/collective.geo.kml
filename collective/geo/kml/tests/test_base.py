import unittest
import doctest

from Testing import ZopeTestCase as ztc

from collective.geo.kml.tests import base


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'README.txt', package='collective.geo.kml',
            test_class=base.CustomStylesFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ztc.FunctionalDocFileSuite(
            'kml-docs.txt', package='collective.geo.kml.tests',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ztc.FunctionalDocFileSuite(
            'folder-kml.txt', package='collective.geo.kml.tests',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ])
