from persistent import Persistent
from zope.interface import implements
from collective.geo.kml.interfaces import IGeoKmlSettings
from zope.component import getUtility

class GeoKmlSettings(Persistent):
    """ 
        GeoKmlSettings ha un po' di proprieta' cui posso accedere direttamente
        >>> config = GeoKmlSettings()
        >>> config.linecolor
        '#FF0000'

        o attraverso il metogo get
        >>> config.get('linewidth')
        2

        posso anche cambiare le proprieta direttamente
        >>> config.polygoncolor = '#FF00FF'
        >>> config.polygoncolor
        '#FF00FF'

        o attraverso il metodo set
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
        comunque questa e' la mia utility
        >>> config = GeoKmlConfig()
        >>> config.getSettings()
        <class 'collective.geo.kml.geokmlconfig.GeoKmlSettings'>

        e queste sono le sue proprieta
        >>> config.getSettings().linewidth
        2

    """
    def getSettings(self):
        return getUtility(IGeoKmlSettings)
