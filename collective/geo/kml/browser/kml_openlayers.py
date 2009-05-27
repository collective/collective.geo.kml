from Products.Five import BrowserView
from collective.geo.openlayers import OpenlayersMessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from collective.geo.settings.interfaces import IGeoSettings


class KmlOpenLayers(BrowserView):
    def __init__(self, context, request):
        super(KmlOpenLayers, self).__init__(context, request)
        self.geosettings = getUtility(IGeoSettings)

    @property
    def zoom(self):
        return  self.geosettings.get('zoom')

    @property
    def googlemaps(self):
        return  self.geosettings.get('googlemaps')

    @property
    def googleapi(self):
        if self.googlemaps:
            return  self.geosettings.get('googleapi')
        return False

    @property
    def map_center(self):
        return  self.geosettings.get('latitude'), self.geosettings.get('longitude')

    def baseJs(self):
        googlemaps = self.googlemaps and 'true' or 'false'
        map_center = self.map_center
        return """
                var lat = %d;
                var lon = %d;
                var googlemaps = %s;
                var zoom = %d;
               """ % (map_center[0],self.map_center[1], googlemaps, self.zoom)

