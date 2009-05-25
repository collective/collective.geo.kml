import zgeo.kml.browser
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from zope.app.pagetemplate import ViewPageTemplateFile
import zgeo.plone.kml.browser
from collective.geo.kml.interfaces import IGeoKmlSettings
from zope.component import getUtility

class Document(zgeo.kml.browser.Document):
    """
        This class extends zgeo.kml.browser.Document class 
        and provide some properties for kml-document from IGeoKmlSettings
        
        Most important properties are linecolor and polygoncolor because converts
        stored data in kml color code.
        
        now we create a TestContent
        >>> from zope import interface
        >>> from zope.dublincore.interfaces import ICMFDublinCore
        >>> class TestContent(object):
        ...     interface.implements(ICMFDublinCore)    
        >>> document = TestContent()
        >>> kmldoc = Document(document, None)
        >>> kmldoc      
        <collective.geo.kml.browser.kml.Document object ...>

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


    def colorconvert(self, color, opacity = 'FF'):
        # color = '#123456'
        r = color[1:3]
        g = color[3:5]
        b = color[5:]
        return opacity + b + g + r
        

document_template = NamedTemplateImplementation(
    ViewPageTemplateFile('kml_document.pt')
    )


class TopicDocument(Document, zgeo.plone.kml.browser.TopicDocument):
    """ Cambio template """


#@property
#def features(self):
#for brain in self.context.queryCatalog():
#yield zgeo.plone.kml.browser.BrainPlacemark(brain, self.request)