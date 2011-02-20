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

        jsfactory = """
        function() { var layer = new OpenLayers.Layer.GML('%s', '%s' + '@@kml-document',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });
            layer.events.on({
                "loadend": function() {
                    layer.map.zoomToExtent(layer.getDataExtent());
            }});
            return layer
            }""" % (self.context.Title().replace("'", "\'"), context_url)

        return unicode(jsfactory, 'utf8')
