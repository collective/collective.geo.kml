from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFPlone.utils import _createObjectByType

@onsetup
def setup_product():
    """
       Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.kml
    zcml.load_config('configure.zcml', collective.geo.kml)

    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['collective.geo.kml'])


#@onsetup
#def setup_plone_kml():
    
    #fiveconfigure.debug_mode = True
    #import collective.geo.kml
    #zcml.load_config('configure.zcml', collective.geo.kml)
    #fiveconfigure.debug_mode = False

#setup_plone_kml()
#ptc.setupPloneSite(products=['collective.geo.kml',])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def afterSetUp(self):
        lpf = self.portal.portal_types['Topic']
        lpf_allow = lpf.global_allow
        lpf.global_allow = True
        lpf = self.portal.portal_types['Large Plone Folder']
        lpf_allow = lpf.global_allow
        lpf.global_allow = True

        self.folder.invokeFactory('Document', 'test-document')
        self.folder['test-document'].setTitle('Test document')
        self.folder['test-document'].setDescription('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend')

        _createObjectByType("Document", self.portal, 'test-document-geostyles')
        _createObjectByType("Topic", self.portal, 'test_topic')
        _createObjectByType("Large Plone Folder", self.portal, 'test_largefolder')

