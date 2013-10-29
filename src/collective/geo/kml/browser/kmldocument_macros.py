from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class KmlDocumentMacros(BrowserView):
    template = ViewPageTemplateFile('kmldocument_macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
