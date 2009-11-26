
from zope.interface import implements

from Products.Five import BrowserView
from Products.CMFCore.interfaces import IFolderish

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
        path = '/'.join(self.context.getPhysicalPath())
        query = {'query': path, 'depth':1}
        for brain in self.context.portal_catalog(path=query, object_provides=IFolderish.__identifier__):
            layers.append(KMLMapLayer(brain.getObject()))
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
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '/@@kml-document',
            { format: OpenLayers.Format.KML,
              projection: cgmap.config['default'].options.displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (self.context.Title().replace("'", "\'"), self.context.absolute_url())
