from zope.interface import Interface, Attribute
from plone.theme.interfaces import IDefaultPloneLayer
from collective.geo.mapwidget.interfaces import IMapView


class IFeature(Interface):
    """http://code.google.com/apis/kml/documentation/kml_tags_beta1.html
    """

    author = Attribute("""A mapping with name, URI, and email keys""")
    id = Attribute("""A universally unique identifier""")
    name = Attribute("""A human readable text""")
    description = Attribute("""A human readable text summary""")
    alternate_link = Attribute("""URL of the resource linked by the entry""")


class IPlacemark(IFeature):
    """http://code.google.com/apis/kml/documentation/kml_tags_beta1.html
    """

    # geographic elements
    coords_kml = Attribute("""KML coordinate encoding of the location""")
    hasLineString = Attribute("""Boolean, True if has a line location""")
    hasPoint = Attribute("""Boolean, True if has a point location""")
    hasPolygon = Attribute("""Boolean, True if has a polygon location""")


class IContainer(IFeature):
    """http://code.google.com/apis/kml/documentation/kml_tags_beta1.html
    """

    features = Attribute("""An iterator over folder and placemark features""")


class IGeoKmlLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IGeoContentKmlView(Interface):
    """ View to access content kml styles """

    def isCustomStyled():
        """Returns True if an object is custom styled"""

    def getStyle(self):
        """ Public function to get object style """


class IKMLOpenLayersView(IMapView):
    """ Marker interface to look up mapwidget manager and layermanager """


class IKMLOpenLayersViewlet(Interface):
    """Marker interface for Viewlet"""
