# -*- coding: utf-8 -*-
from zope.interface import implements

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IWriteGeoreferenced
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle

import collective.geo.kml


CGEO_KML = PloneWithPackageLayer(
    zcml_package=collective.geo.kml,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.geo.kml:default',
    name="CGEO_KML")

CGEO_KML_INTEGRATION = IntegrationTesting(
    bases=(CGEO_KML, ),
    name="CGEO_KML_INTEGRATION")


class KmlFunctionalTesting(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, CGEO_KML)

    def setUpZope(self, app, configurationContext):
        import collective.geo.behaviour
        self.loadZCML(package=collective.geo.behaviour)

    def setUpPloneSite(self, portal):
        super(KmlFunctionalTesting, self).setUpPloneSite(portal)
        applyProfile(portal, 'collective.geo.kml:default')

        # topic_pt = portal.portal_types['Collection']
        # topic_pt.global_allow = True
        # folder_pt = portal.portal_types['Folder']
        # folder_pt.global_allow = True

CGEO_KML_FUNCTIONAL_FIXTURE = KmlFunctionalTesting()

CGEO_KML_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_KML_FUNCTIONAL_FIXTURE, ),
    name="CGEO_KML_FUNCTIONAL")


class CustomStyleManager(object):
    implements(IGeoCustomFeatureStyle)

    use_custom_styles = True
    linecolor = u'FEDCBA3C'
    linewidth = 2.0
    polygoncolor = u'FEDCBA3C'
    marker_image = u'string:${portal_url}/img/marker.png'
    marker_image_size = 1.0
    display_properties = ['Type', 'EffectiveDate', 'ModificationDate']

    def __init__(self, context):
        pass
