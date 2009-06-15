from Products.Five import BrowserView


class KmlOpenLayers(BrowserView):
    """ Kml Openlayers View """

    @property
    def geosettings(self):
        return self.context.restrictedTraverse('@@geosettings-macros')

    @property
    def google_maps_js(self):
        return self.geosettings.google_maps_js

