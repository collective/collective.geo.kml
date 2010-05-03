from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from collective.geo.mapwidget.interfaces import IMapView


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
