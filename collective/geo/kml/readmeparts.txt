    >>> kml_document = self.folder.unrestrictedTraverse('@@kml-document')()
    >>> '<kml xmlns="http://www.opengis.net/kml/2.2">' in kml_document
    True

in that document we have a Placemark from our test-document
    >>> '<name>Test document</name>' in kml_document
    True

we can personalize this view with IGeoKmlSettings
    >>> from collective.geo.kml.interfaces import IGeoKmlSettings
    >>> from zope.component import getUtility
    >>> settings = getUtility(IGeoKmlSettings)
    >>> settings
    <collective.geo.kml.geokmlconfig.GeoKmlSettings object ...>


line width
    >>> settings.linewidth
    2.0

line color
    >>> settings.linecolor
    '#ff0000'


polygon style
    >>> settings.polygoncolor
    '#ff0000'


and points marker
    >>> settings.image_url
    ''
