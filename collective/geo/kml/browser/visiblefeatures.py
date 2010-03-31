from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import utils
from Acquisition import aq_inner
from zgeo.kml.browser import NullGeometry

from collective.geo.kml.browser.document import TopicDocument, Document

class VisibleFeaturesViewlet(ViewletBase):
    def update(self):
        super(VisibleFeaturesViewlet, self).update()
 
        self.displayGeoVisibleFeatures = (self.context.getLayout() == 'kml-openlayers')
        self.form = self.request.form

    def georeferencedContent(self):
        georeferencedFeatures = []
        counter = 0
        for feature in self.features:
            if feature.geom.type is not None:
                georeferencedFeatures.append({'id':counter, 'feature':feature})
            counter += 1
        return georeferencedFeatures
        

    index = ViewPageTemplateFile("visible_features.pt")

class VisibleFeaturesTopicViewlet(VisibleFeaturesViewlet, TopicDocument):
    pass

class VisibleFeaturesFolderViewlet(VisibleFeaturesViewlet, Document):
    pass
