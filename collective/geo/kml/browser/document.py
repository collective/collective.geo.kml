from zope.dublincore.interfaces import ICMFDublinCore
from zope.interface import implements
from zgeo.geographer.interfaces import IGeoreferenced
from zgeo.kml.interfaces import IFeature, IPlacemark, IContainer
from zgeo.kml.browser import NullGeometry
from zgeo.kml.browser import Document as zgeoDocument
from zgeo.kml.browser import Placemark
from Products.CMFCore.utils import getToolByName
from collective.geo.kml.interfaces import IGeoKmlSettings
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from zope.app.pagetemplate import ViewPageTemplateFile
from zgeo.geographer.geo import GeoreferencingAnnotator
from zgeo.kml.browser import NullGeometry

from collective.geo.kml.interfaces import IGeoContentKmlSettings
from collective.geo.kml.config import DISPLAY_VOCABULARY, DISPLAY_PROPERTY_STRUCTURES

import Missing

import logging
logger = logging.getLogger('collective.geo.kml')

@property
def style(self):
    if not self.geo.has_key('style'):
        return False
    return self.geo['style']

GeoreferencingAnnotator.style = style
logger.info("Patching zgeo.geographer.geo's GeoreferencingAnnotator to return custom geo styles.")

NullGeometry.style = None
logger.info("Patching zgeo.kml.browser's NullGeometry to return a None geo style.")

class Document(zgeoDocument):
    """
        This class extends zgeo.kml.browser.Document class
        and provides some properties for kml-document from IGeoKmlSettings

        The most important properties are linecolor and polygoncolor
        because they are converted to kml format
        RRGGBB(web)--->BBGGRRAA(kml)

        now we create a TestContent
        >>> from zope import interface
        >>> from zope.dublincore.interfaces import ICMFDublinCore
        >>> class TestContent(object):
        ...     interface.implements(ICMFDublinCore)
        >>> document = TestContent()
        >>> from collective.geo.kml.interfaces import IGeoContentKmlSettings
        >>> from zope.component import getGlobalSiteManager
        >>> getGlobalSiteManager().registerUtility(document, IGeoContentKmlSettings)
        >>> kmldoc = Document(document, None)
        >>> kmldoc
        <collective.geo.kml.browser.document.Document object ...>

        in GeoKmlSetting we have registered this value for line color
        >>> kmldoc.settings.linecolor
        '#FF0000'

        kml doc must convert web exadecimal code in kml color code
        >>> kmldoc.linecolor
        'FF0000FF'

        the same thing with polygoncolor
        >>> kmldoc.polygoncolor
        '3C0000FF'

        Check to make sure we've also got our style monkey patch in place
        on the annotator and NullGeometry.
        >>> from zgeo.geographer.geo import GeoreferencingAnnotator
        >>> 'style' in dir(GeoreferencingAnnotator)
        True
     
        >>> from zgeo.kml.browser import NullGeometry
        >>> 'style' in dir(NullGeometry)
        True
   
        >>> NullGeometry.style == None
        True

    """
    template = NamedTemplate('geo-kml-document')
    # TODO: set opacity from IGeoKmlSettings
    opacity = '3C'

    def __init__(self, context, request):
        super(Document, self).__init__(context, request)
        self.settings = getUtility(IGeoKmlSettings)
        self.contentkmlsettings = getUtility(IGeoContentKmlSettings)

    @property
    def linecolor(self):
        color = self.settings.linecolor
        if color:
            return self.colorconvert(color)
        return ''

    @property
    def linewidth(self):
        return self.settings.linewidth

    @property
    def polygoncolor(self):
        color = self.settings.polygoncolor
        if color:
            return self.colorconvert(color, self.opacity)
        return ''

    @property
    def pointmarker(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        return '%s/%s' % (portal_state.portal_url(), self.settings.marker_image)

    @property
    def pointmarkersize(self):
        return self.settings.marker_image_size

    #Return a list of dicts of {title: , content: }
    def display_properties(self, item_object):
        selected_properties = []
        custom_styles = self.contentkmlsettings.getStyles(item_object)
        if 'use_custom_style' in custom_styles and custom_styles['use_custom_style'] and 'display_properties' in custom_styles:
            #get our custom results
            selected_properties = custom_styles['display_properties']
        else:
            #get stock-standard from settings
            selected_properties = self.settings.display_properties

        #Fetch our actual information to display on the page
        catalog = getToolByName(item_object,'portal_catalog')
        path = '/'.join(item_object.getPhysicalPath())
        results = catalog.searchResults(path=path,getId=item_object.id,sort_on='created',sort_order='reverse')
        
        properties_to_display = []
        if len(results) > 0:
            rid = results[0].getRID()
            if rid:
                metadata = catalog.getMetadataForRID(rid)

            #iterate through selected properties, and extract data
            #from the object or its catalog metadata
            for property in selected_properties:
                property_title = DISPLAY_VOCABULARY.getTerm(property).title
                
                if metadata.has_key(property):
                    property_content = metadata[property]
                elif hasattr(item_object, property):
                    property_content = getattr(item_object, property)
                    if hasattr(property_content, 'im_func'):
                        property_content = property_content()
                else:
                    property_content = None

		if property in DISPLAY_PROPERTY_STRUCTURES:
                    if len(property_content) > 0:
                        property_content = ', '.join(property_content)
                    else:
                        property_content = None

                if property_content is Missing.Value or property_content is '':
                    property_content = None
                
                properties_to_display.append({
                                       'title': property_title,
                                       'content': str(property_content),
                                     })

        return properties_to_display

    def colorconvert(self, color, opacity = 'FF'):
        # color = '#123456'
        r = color[1:3]
        g = color[3:5]
        b = color[5:]
        return opacity + b + g + r

document_template = NamedTemplateImplementation(
    ViewPageTemplateFile('kml_document.pt')
    )


class Geometry(object):
    
    implements(IGeoreferenced)

    def __init__(self, type, coordinates, style):
        self.type = type
        self.coordinates = coordinates
        self.style = style


class BrainPlacemark(Placemark):

    implements(IPlacemark)
    __name__ = 'kml-placemark'

    def __init__(self, context, request):
	self.context = context
        self.dc = context.getObject()
        self.request = request
        try:
            g = self.context.zgeo_geometry
            self.geom = Geometry(g['type'], g['coordinates'], g['style'])
        except:
            self.geom = NullGeometry()

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
            'email': ''
            }

    @property
    def alternate_link(self):
        return '/'.join(
            [self.request['BASE1']] 
            + self.request.physicalPathToVirtualPath(self.context.getPath())
            )


class TopicDocument(Document):

    @property
    def features(self):
        for brain in self.context.queryCatalog():
            yield BrainPlacemark(brain, self.request)
