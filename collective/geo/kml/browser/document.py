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
    """
    template = NamedTemplate('geo-kml-document')
    # TODO: set opacity from IGeoKmlSettings
    opacity = '3C'

    def __init__(self, context, request):
        super(Document, self).__init__(context, request)
        self.settings = getUtility(IGeoKmlSettings)

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

    def __init__(self, type, coordinates):
        self.type = type
        self.coordinates = coordinates


class BrainPlacemark(Placemark):

    implements(IPlacemark)
    __name__ = 'kml-placemark'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        try:
            g = self.context.zgeo_geometry
            self.geom = Geometry(g['type'], g['coordinates'])
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
