from zope.interface import implements
from zope.component import getUtility

from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.settings.interfaces import IGeoSettings

from collective.geo.mapwidget.browser.widget import MapLayers

from collective.geo.kml.browser.maplayers import KMLMapLayer
from collective.geo.kml.interfaces import IKMLOpenLayersViewlet


class ContentViewlet(ViewletBase):
    implements(IKMLOpenLayersViewlet)


    @property
    def display_manager(self):
        dm = IGeoCustomFeatureStyle(self.context).map_display_manager
        if dm:
            return dm
        else:
            defaultstyles = getUtility(IRegistry).forInterface(IGeoSettings)
            type_defaults = defaultstyles.map_display_manager_types
            td_dict = {}
            for td in type_defaults:
                k,v = td.split(':')
                td_dict[k]=v
            if self.context.portal_type in td_dict.keys():
                return td_dict[self.context.portal_type]
            else:
                return defaultstyles.default_manager


    @property
    def coordinates(self):
        return IGeoreferenced(self.context)

    def render(self):
        display_manager = self.display_manager
        if self.manager.__name__ == display_manager:
            coords = self.coordinates
            if coords.type and coords.coordinates:
                return super(ContentViewlet, self).render()
            else:
                return ''
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
