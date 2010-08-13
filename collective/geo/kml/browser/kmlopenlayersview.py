from zope.interface import implements

from Products.Five import BrowserView
from Products.CMFCore.interfaces import IFolderish

from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer

from collective.geo.kml.interfaces import IKMLOpenLayersView


class KmlOpenLayersView(BrowserView):
    """ Kml Openlayers View """

    implements(IKMLOpenLayersView)


class KMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(self.context))
        # TODO: for each sub folder or collection creat new layer (sublayer)
        path = '/'.join(self.context.getPhysicalPath())
        query = {'query': path, 'depth': 1}
        for brain in self.context.portal_catalog(path=query,
                                object_provides=IFolderish.__identifier__):
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
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return"""
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '@@kml-document',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (self.context.Title().replace("'", "\'"), context_url)
