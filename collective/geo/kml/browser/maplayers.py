from collective.geo.mapwidget.maplayers import MapLayer


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
            });}""" % (self.context.Title().decode('utf-8', 'ignore'
                                ).encode('ascii', 'xmlcharrefreplace'
                                ).replace("'", "\'"), context_url)

