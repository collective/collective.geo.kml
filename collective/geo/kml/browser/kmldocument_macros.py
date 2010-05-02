from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView


class KmlDocumentMacros(BrowserView):
    template = ViewPageTemplateFile('kmldocument_macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
