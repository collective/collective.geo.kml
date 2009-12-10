from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import utils
from Acquisition import aq_inner

class VisibleFeaturesViewlet(ViewletBase):
    def update(self):
        super(VisibleFeaturesViewlet, self).update()
 
        self.displayGeoVisibleFeatures = (self.context.getLayout() == 'kml-openlayers')
        self.form = self.request.form

    @property
    def uniqueItemIndex(self):
        return utils.RealIndexIterator(pos=0)

    index = ViewPageTemplateFile("visible_features.pt")
