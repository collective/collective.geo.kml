from persistent import Persistent
from zope.interface import implements, implementsOnly
from zope.schema.fieldproperty import FieldProperty
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

from collective.geo.kml.interfaces import IGeoKmlSettings, IGeoContentKmlSettings
from zgeo.geographer.geo import KEY

class GeoKmlSettings(Persistent):
    """ 
        GeoKmlSettings have some propreties. We can get its propterties directly
        >>> config = GeoKmlSettings()
        >>> config.linecolor
        '#FF0000'

        or by the 'get' method
        >>> config.get('linewidth')
        2.0

        we can set GeoKmlSettings in this way
        >>> config.polygoncolor = '#FF00FF'
        >>> config.polygoncolor
        '#FF00FF'

        or by the 'set' method
        >>> config.set('marker_image', 'marker-blue.png')
        >>> config.marker_image
        'marker-blue.png'
 
        >>> config.set('marker_image_size', 1.0)
        >>> config.marker_image_size
        1.0

    """ 
    implements(IGeoKmlSettings)

    linecolor = '#FF0000'
    linewidth = 2.0
    polygoncolor = '#FF0000'
    marker_image = 'img/marker.png'
    marker_image_size = 0.7

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
        2.0

    """
    def getSettings(self):
        return getUtility(IGeoKmlSettings)


class GeoContentKmlSettings(Persistent):
    """ """ 
    implements(IGeoContentKmlSettings)

    def __init__(self, context=None, form=None):
        self.context = context
        self.form = form

    def initialiseStyles(self, context):
        annotations = IAnnotations(context)
        geo = annotations.get(KEY)
        if geo:
            self.geo_styles = geo.get('style')

            if not self.geo_styles:
                geo['style'] = {}
                self.geo_styles = geo['style']
                self.geo_styles['use_custom_style'] = False
                self.geo_styles['linecolor'] = u'#FF0000'
                self.geo_styles['linewidth'] = 2.0
                self.geo_styles['polygoncolor'] = u'#FF0000'
                self.geo_styles['marker_image'] = u'img/marker.png'
                self.geo_styles['marker_image_size'] = 0.7
        else:
            self.geo_styles = {}

    def set(self, key,  val):
        return self.geo_styles.__setitem__(key, val)

    def getStyles(self, context):
        self.initialiseStyles(context)
        return self.geo_styles

    def get(self, key,  default=False):
        try:
            return self.geo_styles.get(key)
        except:
            return default

