# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.interface import alsoProvides

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IWriteGeoreferenced
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle

import collective.geo.kml


CGEO_KML = PloneWithPackageLayer(
    zcml_package=collective.geo.kml,
    zcml_filename='configure.zcml',
    gs_profile_id='collective.geo.kml:default',
    name="CGEO_KML")

CGEO_KML_INTEGRATION = IntegrationTesting(
    bases=(CGEO_KML, ),
    name="CGEO_KML_INTEGRATION")


class KmlFunctionalTesting(PloneSandboxLayer):

    defaultBases = (CGEO_KML,)

    def setUpPloneSite(self, portal):
        super(KmlFunctionalTesting, self).setUpPloneSite(portal)

        topic_pt = portal.portal_types['Topic']
        topic_pt.global_allow = True
        # folder_pt = portal.portal_types['Folder']
        # folder_pt.global_allow = True


CGEO_KML_FUNCTIONAL_FIXTURE = KmlFunctionalTesting()

CGEO_KML_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_KML_FUNCTIONAL_FIXTURE, ),
    name="CGEO_KML_FUNCTIONAL")


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
