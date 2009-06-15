from z3c.form import field, form, button
from plone.z3cform import z2

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility
from zope.app.component.hooks import getSite

from collective.geo.kml.interfaces import IGeoKmlSettings
from collective.geo.kml import GeoKmlMessageFactory as _

def geo_kml_settings(context):
    return getUtility(IGeoKmlSettings)

def back_to_controlpanel(self):
    root = getSite()
    return dict(url=root.absolute_url() + '/plone_control_panel')

from collective.z3cform.colorpicker.colorpicker import ColorpickerFieldWidget
class GeoKmlControlpanelForm(form.EditForm):
    fields = field.Fields(IGeoKmlSettings)
    fields['linecolor'].widgetFactory = ColorpickerFieldWidget
    fields['polygoncolor'].widgetFactory = ColorpickerFieldWidget

    heading = _(u'Geo kml settings')

    @button.handler(form.EditForm.buttons['apply'])
    def handle_add(self, action):
        data, errors = self.extractData()
        if errors:
            return

        utility = getUtility(IGeoKmlSettings)
        for key, val in data.items():
            utility.set(key, val)

class GeoKmlControlpanel(BrowserView):
    __call__ = ViewPageTemplateFile('controlpanel.pt')

    label = _(u'Geo Kml')
    description = _(u"Geo Kml default settings")
    back_link = back_to_controlpanel

    def contents(self):
        z2.switch_on(self)
        form = GeoKmlControlpanelForm(self.context, self.request)
        form.update()
        return form.render()
