from plone.memoize.instance import memoizedproperty
from collective.geo.mapwidget.maplayers import MapLayer


class KMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """
    name = 'kml'

    @memoizedproperty
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        template = self.context.restrictedTraverse('%s-layer' % self.name)()
        return template % (self.context.Title().replace("'", "\'"),
                           context_url)
