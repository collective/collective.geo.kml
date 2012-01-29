from zope.interface import implements, alsoProvides

# from Products.Five import zcml
from Zope2.App import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFPlone.utils import _createObjectByType

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.geographer.interfaces import IGeoreferenceable


@onsetup
def setup_product():
    """Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.kml
    zcml.load_config('configure.zcml', collective.geo.kml)

    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(extension_profiles=('collective.geo.kml:default', ))


class CustomStyleManager(object):
    implements(IGeoCustomFeatureStyle)

    geostyles = {
     'use_custom_styles': True,
     'linecolor': u'FEDCBA3C',
     'linewidth': 2.0,
     'polygoncolor': u'FEDCBA3C',
     'marker_image': u'string:${portal_url}/img/marker.png',
     'marker_image_size': 1.0,
     'display_properties': ['Type', 'EffectiveDate', 'ModificationDate'],
    }

    def __init__(self, context):
        pass


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def afterSetUp(self):
        topic_pt = self.portal.portal_types['Topic']
        topic_pt.global_allow = True
        folder_pt = self.portal.portal_types['Folder']
        folder_pt.global_allow = True

        self.folder.invokeFactory('Document', 'test-document')
        self.folder['test-document'].setTitle('Test document')
        self.folder['test-document'].setDescription(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '\
                'Maecenas malesuada, sapien non tincidunt semper, elit '\
                'tortor varius neque, non fringilla dui nisi ac lacus. '\
                'Aliquam erat volutpat. Etiam lobortis pharetra eleifend')

        _createObjectByType("Document", self.portal, 'test-document-geostyles')
        _createObjectByType("Topic", self.portal, 'test_topic')
        _createObjectByType("Folder", self.portal, 'test_folder')

        # provide IGeoreferenceable interface to document created
        alsoProvides(self.folder['test-document'], IGeoreferenceable)
        alsoProvides(self.portal['test-document-geostyles'], IGeoreferenceable)


class CustomStylesFunctionalTestCase(FunctionalTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def afterSetUp(self):
        super(CustomStylesFunctionalTestCase, self).afterSetUp()
        # register adapter for custom styles

    def tearDown(self):
        # unregister the previous adapter
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(CustomStyleManager,
                                (IGeoreferenceable,), IGeoCustomFeatureStyle)
