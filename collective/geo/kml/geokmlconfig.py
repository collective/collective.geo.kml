from persistent import Persistent
from zope.interface import implements
from collective.geo.kml.interfaces import IGeoKmlSettings
from zope.component import getUtility

class GeoKmlSettings(Persistent):
    """ 
        GeoKmlSettings have some propreties. We can get its propterties directly
        >>> config = GeoKmlSettings()
        >>> config.linecolor
        '#FF0000'

        or by the 'get' method
        >>> config.get('linewidth')
        2

        we can set GeoKmlSettings in this way
        >>> config.polygoncolor = '#FF00FF'
        >>> config.polygoncolor
        '#FF00FF'

        or by the 'set' method
        >>> config.set('marker_image', 'marker-blue.png')
        >>> config.marker_image
        'marker-blue.png'

    """ 
    implements(IGeoKmlSettings)

    linecolor = '#FF0000'
    linewidth = 2
    polygoncolor = '#FF0000'
    marker_image = 'marker.png'

    def set(self, key,  val):
        return self.__setattr__(key, val)

    def get(self, key,  default=False):
        try:
            return self.__getattribute__(key)
        except:
            return default

class GeoKmlConfig(object):
    """
        Non ho ancora capito a cosa serva sto coso
        We get the IGeoKmlSettings utility
        >>> config = GeoKmlConfig()
        >>> config.getSettings()
        <class 'collective.geo.kml.geokmlconfig.GeoKmlSettings'>

        and its properties
        >>> config.getSettings().linewidth
        2

    """
    def getSettings(self):
        return getUtility(IGeoKmlSettings)
