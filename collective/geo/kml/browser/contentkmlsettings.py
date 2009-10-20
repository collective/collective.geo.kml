from zope.component import getUtility

from collective.geo.kml.interfaces import IGeoContentKmlSettings

def geo_content_kml_settings(context):
    return getUtility(IGeoContentKmlSettings)

