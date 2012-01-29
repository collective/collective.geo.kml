from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.component import getUtility

from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.dublincore.interfaces import ICMFDublinCore
from zope.publisher.browser import BrowserPage

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.Expression import Expression, getExprContext
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.settings import DISPLAY_PROPERTIES_DATES

from collective.geo.kml.interfaces import IFeature, IContainer, IPlacemark
from collective.geo.kml.utils import web2kmlcolor
import cgi

# support to collective.contentleadimage
has_leadimage = True
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
except:
    has_leadimage = False


def get_marker_image(context, marker_img):
    try:
        marker_img = Expression(str(marker_img))(getExprContext(context))
    except:
        marker_img = ''
    return marker_img


def absoluteURL(ob, request):
    return getMultiAdapter((ob, request), IAbsoluteURL)()


def coords_to_kml(geom):
    gtype = geom.type
    coordlist = []
    if gtype == 'Point':
        coords = (geom.coordinates,)
        coordlist.append(coords)
    elif gtype == 'Polygon':
        coords = geom.coordinates[0]
        coordlist.append(coords)
    elif gtype == 'LineString':
        coords = geom.coordinates
        coordlist.append(coords)
    elif gtype == 'MultiPoint':
        coordlist = [[g, ] for g in geom.coordinates]
    elif gtype == 'MultiPolygon':
        coordlist = [c[0] for c in geom.coordinates]
    elif gtype == 'MultiLineString':
        coordlist = geom.coordinates
    else:
        raise ValueError("Invalid geometry type")
    coords_kml = []
    for coordinates in coordlist:
        if len(coordinates[0]) == 2:
            tuples = ('%f,%f,0.0' % tuple(c) for c in coordinates)
        elif len(coordinates[0]) == 3:
            tuples = ('%f,%f,%f' % tuple(c) for c in coordinates)
        else:
            raise ValueError("Invalid dimensions")
        coords_kml.append(' '.join(tuples))
    if gtype in ['Point', 'Polygon', 'LineString']:
        return coords_kml[0]
    else:
        return coords_kml


class NullGeometry(object):
    type = None
    coordinates = None


class Feature(BrowserPage):
    """Not to be instantiated.
    """
    implements(IFeature)

    @property
    def id(self):
        return '%s/@@%s' % (absoluteURL(self.context, self.request),
                            self.__name__)

    @property
    def name(self):
        return self.dc.Title()

    @property
    def description(self):
        return cgi.escape(self.dc.Description())

    @property
    def author(self):
        return {
            'name': self.dc.Creator(),
            'uri': '',
            'email': ''
            }

    @property
    def alternate_link(self):
        return absoluteURL(self.context, self.request)


class Placemark(Feature):
    implements(IPlacemark)
    __name__ = 'kml-placemark'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dc = ICMFDublinCore(self.context)
        try:
            self.geom = IGeoreferenced(self.context)
        except:
            self.geom = NullGeometry()

        try:
            self.styles = IGeoFeatureStyle(context).geostyles
        except:
            self.styles = None

    def __call__(self):
        return self.template().encode('utf-8')

    @property
    def hasPoint(self):
        return int(self.geom.type == 'Point')

    @property
    def hasLineString(self):
        return int(self.geom.type == 'LineString')

    @property
    def hasPolygon(self):
        return int(self.geom.type == 'Polygon')

    @property
    def hasMultiPoint(self):
        return int(self.geom.type == 'MultiPoint')

    @property
    def hasMultiLineString(self):
        return int(self.geom.type == 'MultiLineString')

    @property
    def hasMultiPolygon(self):
        return int(self.geom.type == 'MultiPolygon')

    @property
    def coords_kml(self):
        try:
            return coords_to_kml(self.geom)
        except:
            pass

    @property
    def properties_vocabulary_labels(self):
        terms = getUtility(IVocabularyFactory,
                    name="displaypropertiesVocab").terms
        labels = {}
        for k, v in terms:
            labels[k] = v
        return labels

    @property
    def use_custom_styles(self):
        if not self.styles:
            return False
        return self.styles.get('use_custom_styles', False)

    @property
    def linecolor(self):
        if self.styles:
            return web2kmlcolor(self.styles['linecolor'])
        return u''

    @property
    def linewidth(self):
        if self.styles:
            return self.styles['linewidth']
        return ''

    @property
    def polygoncolor(self):
        if self.styles:
            return web2kmlcolor(self.styles['polygoncolor'])
        return u''

    @property
    def marker_image(self):
        if self.styles:
            return get_marker_image(self.context, self.styles['marker_image'])
        return u''

    @property
    def marker_image_size(self):
        if self.styles:
            return self.styles['marker_image_size']
        return u''

    @property
    def item_type(self):
        if callable(self.dc.portal_type):
            return self.dc.portal_type()
        else:
            return self.dc.portal_type

    @property
    def item_url(self):
        return self.dc.absolute_url()

    def display_properties(self, document):
        properties = document.display_properties
        if self.styles and self.use_custom_styles:
            properties = self.styles['display_properties']
        return [(self.properties_vocabulary_labels.get(prop, prop),
                        self.getDisplayValue(prop)) for prop in properties]

    def getDisplayValue(self, prop):
        return self.formatDisplayProperty(getattr(self.context, prop), prop)

    def formatDisplayProperty(self, value, prop):
        # value could be a bound method...
        try:
            value = value()
        except:
            pass

        # value could be a string representing a date
        if prop in DISPLAY_PROPERTIES_DATES:
            return self.context.toLocalizedTime(value, long_format=1)

        if isinstance(value, tuple) or\
                        isinstance(value, list):
            return ' '.join(value)

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            string = ''
            for k, v in value.items():
                string += str(k) + ': ' + str(v)
            return string
        return value

    def lead_image(self, scale='thumb', css_class="tileImage"):
        #is brain?
        try:
            obj = self.context.getObject()
        except AttributeError:
            obj = self.context

        try:
            image_field = obj.getField('image')
        except:
            return None

        if has_leadimage and not image_field:
            image_field = obj.getField(IMAGE_FIELD_NAME)

        if image_field and image_field.get_size(obj):
            return image_field.tag(obj, scale=scale, css_class=css_class)
        return None


class Folder(Feature):

    implements(IContainer)
    __name__ = 'kml-folder'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dc = ICMFDublinCore(self.context)

    @property
    def features(self):
        for item in self.context.values():
            yield Placemark(item, self.request)


class BrainPlacemark(Placemark):

    implements(IPlacemark)
    __name__ = 'kml-placemark'

    def __init__(self, context, request, document):
        self.context = context
        self.request = request
        self.geom = NullGeometry()
        if context.zgeo_geometry:
            self.geom.type = context.zgeo_geometry['type']
            self.geom.coordinates = context.zgeo_geometry['coordinates']
        try:
            self.styles = self.context.collective_geo_styles
        except:
            self.styles = None

    @property
    def id(self):
        return 'urn:uuid:%s' % self.context.UID

    @property
    def name(self):
        return self.context.Title

    @property
    def description(self):
        return self.context.Description

    @property
    def author(self):
        return {
            'name': self.context.Creator,
            'uri': '',
            'email': ''}

    def getDisplayValue(self, prop):
        return self.formatDisplayProperty(getattr(self.context, prop), prop)

    @property
    def item_type(self):
        return self.context.portal_type

    @property
    def item_url(self):
        return self.context.getURL()


class KMLBaseDocument(Feature):
    """This class extends Feature class
    and provides some properties for kml-document from IGeoFeatureStyle
    """
    implements(IContainer)
    __name__ = 'kml-document'
    template = ViewPageTemplateFile('kmldocument.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dc = ICMFDublinCore(self.context)
        registry = getUtility(IRegistry)
        self.styles = registry.forInterface(IGeoFeatureStyle)

    @property
    def features(self):
        raise NotImplementedError

    def __call__(self):
        # bha! --- Internet explorer cache the kml-document
        # self.request.RESPONSE.setHeader('Cache-Control','max-age=3600')
        # self.request.RESPONSE.setHeader(
        #               'Expires','Thu, 01 Aug 2000 09:00:00 GMT')
        # self.request.RESPONSE.setHeader(
        #               'Last-Modified', 'Thu, 01 Aug 2000 09:00:00 GMT')
        # self.request.RESPONSE.setHeader('Pragma', 'no-cache')
        return self.template().encode('utf-8')

    @property
    def linecolor(self):
        return web2kmlcolor(self.styles.linecolor)

    @property
    def linewidth(self):
        return self.styles.linewidth

    @property
    def polygoncolor(self):
        return web2kmlcolor(self.styles.polygoncolor)

    @property
    def marker_image(self):
        return get_marker_image(self.context, self.styles.marker_image)

    @property
    def marker_image_size(self):
        return self.styles.marker_image_size

    @property
    def display_properties(self):
        return self.styles.display_properties


class KMLDocument(KMLBaseDocument):

    @property
    def features(self):
        feature = queryMultiAdapter((self.context, self.request), IFeature)
        if feature:
            return [feature]
        return []


class KMLFolderDocument(KMLBaseDocument):

    @property
    def features(self):
        for item in self.context.values():
            feature = queryMultiAdapter((item, self.request), IFeature)
            if not feature:
                continue
            yield feature


class KMLTopicDocument(KMLBaseDocument):

    @property
    def features(self):
        for brain in self.context.queryCatalog():
            yield BrainPlacemark(brain, self.request, self)
