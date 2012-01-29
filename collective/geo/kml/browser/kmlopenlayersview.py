from zope.interface import implements

from Products.Five import BrowserView
from Products.CMFCore.interfaces import IFolderish

from collective.geo.mapwidget.browser.widget import MapLayers

from collective.geo.kml.browser.maplayers import KMLMapLayer
from collective.geo.kml.interfaces import IKMLOpenLayersView


class KmlOpenLayersView(BrowserView):
    """ Kml Openlayers View """

    implements(IKMLOpenLayersView)


class KMLMapLayers(MapLayers):
    '''create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(context=self.context))
        # TODO: for each sub folder or collection create new layer (sublayer)
        path = '/'.join(self.context.getPhysicalPath())
        query = {'query': path, 'depth': 1}
        for brain in self.context.portal_catalog(path=query,
                                object_provides=IFolderish.__identifier__):
            layers.append(KMLMapLayer(context=brain.getObject()))
        return layers
