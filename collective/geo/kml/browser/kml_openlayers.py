from Products.Five import BrowserView
from collective.geo.kml import GeoKmlMessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from collective.geo.settings.interfaces import IGeoSettings


class KmlOpenLayers(BrowserView):
    """ Kml Openlayers View """

    @property
    def geosettings(self):
        return self.context.restrictedTraverse('@@geosettings-macros')

    @property
    def google_maps_js(self):
        return self.geosettings.google_maps_js

