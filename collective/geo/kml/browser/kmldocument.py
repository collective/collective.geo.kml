from zope.interface import implements

from zope.component import getMultiAdapter
from zope.component import getUtility

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.schema.vocabulary import IVocabularyFactory

from plone.registry.interfaces import IRegistry

from zgeo.geographer.interfaces import IGeoreferenced

from zgeo.kml.interfaces import IPlacemark
import zgeo.kml.browser

from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.kml.utils import web2kmlcolor
from collective.geo.settings import DISPLAY_PROPERTIES_DATES


# # support to collective.contentleadimage
has_leadimage = True
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
except:
    has_leadimage = False


class Placemark(zgeo.kml.browser.Placemark):

    def __init__(self, context, request):
        super(Placemark, self).__init__(context, request)
        try:
            self.styles = IGeoFeatureStyle(context).geostyles
        except:
            self.styles = None

    @property
    def coords_kml(self):
        try:
            return zgeo.kml.browser.coords_to_kml(self.geom)
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
            portal_state = getMultiAdapter((self.context, self.request),
                                                    name=u"plone_portal_state")
            return '%s/%s' % (portal_state.portal_url(),
                                    self.styles['marker_image'])

        return u''

    @property
    def marker_image_size(self):
        if self.styles:
            return self.styles['marker_image_size']
        return u''

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

        image_field = obj.getField('image')
        if has_leadimage and not image_field:
            image_field = obj.getField(IMAGE_FIELD_NAME)

        if image_field:
            return image_field.tag(obj, scale=scale, css_class=css_class)
        return None


class KMLDocument(zgeo.kml.browser.Document):
    """
        This class extends zgeo.kml.browser.Document class
        and provides some properties for kml-document from IGeoFeatureStyle
    """
    template = ViewPageTemplateFile('kmldocument.pt')

    def __init__(self, context, request):
        super(KMLDocument, self).__init__(context, request)
        registry = getUtility(IRegistry)
        self.styles = registry.forInterface(IGeoFeatureStyle)

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
        portal_state = getMultiAdapter((self.context, self.request),
                                                name=u"plone_portal_state")
        return '%s/%s' % (portal_state.portal_url(),
                                self.styles.marker_image)

    @property
    def marker_image_size(self):
        return self.styles.marker_image_size

    @property
    def display_properties(self):
        return self.styles.display_properties


class BrainPlacemark(Placemark):

    implements(IPlacemark)
    __name__ = 'kml-placemark'

    def __init__(self, context, request, document):
        self.context = context
        self.request = request
        self.dc = context.getObject()
        try:
            self.geom = IGeoreferenced(self.dc)
        except:
            self.geom = zgeo.kml.browser.NullGeometry()

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


class KMLTopicDocument(KMLDocument):

    @property
    def features(self):
        for brain in self.context.queryCatalog():
            yield BrainPlacemark(brain, self.request, self)
