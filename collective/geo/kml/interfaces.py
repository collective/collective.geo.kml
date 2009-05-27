from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope import schema
from collective.geo.kml import GeoKmlMessageFactory as _

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

    linewidth = schema.Int(title=_(u"Line width"),
                          description=_(u"Default line width in pixel"),
                          default=2,
                          required=True)

    polygoncolor = schema.TextLine(title=_(u"Polygon color"),
                          description=_(u"Default polygon color"),
                          default=u'#ff0000',
                          required=False)

    marker_image = schema.TextLine(title=_(u"Marker image"),
                          description=_(u"Default point marker image"),
                          required=False)