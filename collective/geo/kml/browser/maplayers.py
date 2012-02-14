from plone.memoize.instance import memoizedproperty
from collective.geo.mapwidget.maplayers import MapLayer


class KMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """
    name = 'kml'

    @memoizedproperty
    def jsfactory(self):
        title = self.context.Title().replace("'", "\\'")
        if isinstance(title, str):
            title = title.decode('utf-8')
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        template = self.context.restrictedTraverse('%s-layer' % self.name)()
        return template % (title, context_url)
