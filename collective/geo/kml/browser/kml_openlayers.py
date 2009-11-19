
from zope.interface import implements

from Products.Five import BrowserView

from collective.geo.settings.browser.widget import MapLayers, MapLayer

from collective.geo.kml.interfaces import IGeoKMLOpenLayersView

class KmlOpenLayers(BrowserView):
    """ Kml Openlayers View """

    implements(IGeoKMLOpenLayersView)

    # @property
    # def geosettings(self):
    #     return self.context.restrictedTraverse('@@geosettings-view')

    # @property
    # def google_maps_js(self):
    #     return self.geosettings.google_maps_js

class KMLMapLayers(MapLayers):

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(self.context))
        # TODO: for each sub folder or collection creat new layer (sublayer)
        return layers

class KMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        return"""
        function() { return new OpenLayers.Layer.GML('KML Layer', '%s' + '/@@kml-document',
            { format: OpenLayers.Format.KML,
              projection: cgmap.config['default'].options.displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (self.context.absolute_url())

class KMLSubMapLayer(MapLayer):
    """
    a layer to collect features of sub folders
    """
