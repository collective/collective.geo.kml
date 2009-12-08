from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VisibleFeaturesViewlet(ViewletBase):
    def update(self):
        super(VisibleFeaturesViewlet, self).update()
 
        self.displayGeoVisibleFeatures = (self.context.getLayout() == 'kml-openlayers')

    index = ViewPageTemplateFile("visible_features.pt")
