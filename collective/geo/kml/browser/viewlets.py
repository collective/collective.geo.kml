from zope.interface import implements
from zope.component import getUtility
from zope.component import queryAdapter

from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.settings.interfaces import (
                                        IGeoCustomFeatureStyle,
                                        IGeoFeatureStyle)

from collective.geo.mapwidget.browser.widget import MapLayers


from collective.geo.kml.browser.maplayers import KMLMapLayer as BaseLayer
from collective.geo.kml.interfaces import IKMLOpenLayersViewlet


class KMLMapLayer(BaseLayer):
    name = 'kmlviewlet'


class ContentViewlet(ViewletBase):
    implements(IKMLOpenLayersViewlet)

    @property
    def coordinates(self):
        return IGeoreferenced(self.context)

    @property
    def map_viewlet_position(self):
        custom_styles = queryAdapter(self.context, IGeoCustomFeatureStyle)
        if custom_styles and custom_styles.use_custom_styles:
            return custom_styles.map_viewlet_position
        else:
            defaultstyles = getUtility(IRegistry).forInterface(
                                                    IGeoFeatureStyle)
            return defaultstyles.map_viewlet_position

    def render(self):
        if self.manager.__name__ != self.map_viewlet_position:
            return ''

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
        layers.append(KMLMapLayer(context=self.context))
        return layers
