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
    import zgeo.plone.kml
    zcml.load_config('configure.zcml', zgeo.plone.kml)

    fiveconfigure.debug_mode = False

    #ztc.installPackage('collective.geo.kml')
    ztc.installPackage('zgeo.plone.kml')

setup_product()
ptc.setupPloneSite(products=['collective.geo.kml'])

class KmlTestCase(ptc.PloneTestCase):
    pass


class KmlFunctionalTestCase(ptc.FunctionalTestCase):

    def afterSetUp(self):
        """
            Creating some contents in the portal
        """
        self.folder.invokeFactory('Document', 'test-document')
        self.folder['test-document'].setTitle('Test document')
        self.folder['test-document'].setDescription('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend')

        _createObjectByType("Topic", self.portal, 'test_topic')
        _createObjectByType("Large Plone Folder", self.portal, 'test_largefolder')




