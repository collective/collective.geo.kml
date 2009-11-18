from persistent import Persistent
from zope.interface import implements, implementsOnly
from zope.schema.fieldproperty import FieldProperty
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

from collective.geo.kml.interfaces import IGeoKmlSettings, IGeoContentKmlSettings
from zgeo.geographer.geo import KEY

from Products.CMFCore.utils import getToolByName

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

        >>> config.set('display_properties', ['Type', 'CreationDate'])
        >>> config.display_properties
        ['Type', 'CreationDate']

    """ 
    implements(IGeoKmlSettings)

    linecolor = '#FF0000'
    linewidth = 2.0
    polygoncolor = '#FF0000'
    marker_image = u'img/marker.png'
    marker_image_size = 0.7
    display_properties = ['id', 'Type']

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

        if self.context is not None:
            #get our site's config to set the default values from it
            portal_url = getToolByName(self.context, 'portal_url')
            portal = portal_url.getPortalObject()
            self.siteconfig = IGeoKmlSettings(portal)
        else:
            self.siteconfig = None

    def initialiseStyles(self, context):
        annotations = IAnnotations(context)
        geo = annotations.get(KEY)
        if geo:
            self.geo_styles = geo.get('style')

            if not self.geo_styles:
                geo['style'] = {}
                self.geo_styles = geo['style']
                self.geo_styles['use_custom_style'] = False

                if self.siteconfig is not None:
                    self.geo_styles['linecolor'] = self.siteconfig.get('linecolor')
                    self.geo_styles['linewidth'] = self.siteconfig.get('linewidth')
                    self.geo_styles['polygoncolor'] = self.siteconfig.get('polygoncolor')
                    self.geo_styles['marker_image'] = self.siteconfig.get('marker_image')
                    self.geo_styles['marker_image_size'] = self.siteconfig.get('marker_image_size')
                    self.geo_styles['display_properties'] = self.siteconfig.get('display_properties')
                else:
                    self.geo_styles['linecolor'] = '#FF0000'
                    self.geo_styles['linewidth'] = 2.0
                    self.geo_styles['polygoncolor'] = '#FF0000'
                    self.geo_styles['marker_image'] = u'img/marker.png'
                    self.geo_styles['marker_image_size'] = 0.7
                    self.geo_styles['display_properties'] = ['id', 'Type']
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

