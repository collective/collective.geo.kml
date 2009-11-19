from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope import schema
from collective.geo.kml import GeoKmlMessageFactory as _

from collective.geo.settings.interfaces import IMapView

class IGeoKmlLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
class IGeoKmlConfig(Interface):
    """ marker interface """

class IGeoKmlSettings(Interface):
    linecolor = schema.TextLine(title=_(u"Line color"),
                          description=_(u"Default line color"),
                          default=u'#ff0000',
                          required=True)

    linewidth = schema.Float(title=_(u"Line width"),
                          description=_(u"Default line width in pixels"),
                          default=2.0,
                          required=True)

    polygoncolor = schema.TextLine(title=_(u"Polygon color"),
                          description=_(u"Default polygon color"),
                          default=u'#ff0000',
                          required=False)

    marker_image = schema.TextLine(title=_(u"Marker image"),
                          description=_(u"Default point marker image"),
                          default=u'img/marker.png',
                          required=False)

    marker_image_size = schema.Float(title=_(u"Marker image size"),
                          description=_(u"Scaled size of the marker image"),
                          default=0.7,
                          required=True)


class IGeoContentKmlView(Interface):
    """ View to access content kml styles """
    def isCustomStyled():
        """Returns True if an object is custom styled"""

    def getStyle(self):
        """ Public function to get object style """

class IGeoContentKmlForm(Interface):
    """ Interface for style management form """

class IGeoContentKmlSettings(IGeoKmlSettings):
    """ Interface for content-specific KML settings """

    use_custom_style = schema.Bool(title=_(u"Use custom styles"),
                         description=_(u"Select this if you want to use a custom style on the map for this content item.  This overrides any default style set."),
                         default=False,
                         required=False)

class IGeoKMLOpenLayersView(IMapView):
    """ Marker interface to look up mapwidget manager and layermanager """
