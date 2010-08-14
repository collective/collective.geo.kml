from zope.interface import implements
from plone.app.layout.viewlets import ViewletBase
from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.mapwidget.browser.widget import MapLayers

from collective.geo.kml.browser.maplayers import KMLMapLayer
from collective.geo.kml.interfaces import IKMLOpenLayersViewlet


class ContentViewlet(ViewletBase):
    implements(IKMLOpenLayersViewlet)

    @property
    def coordinates(self):
        return IGeoreferenced(self.context)

    def render(self):
        coords = self.coordinates
        if coords.type and coords.coordinates:
            return super(ContentViewlet, self).render()
        else:
            return ''


class KMLMapViewletLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapViewletLayers, self).layers()
        layers.append(KMLMapLayer(self.context))
        return layers
