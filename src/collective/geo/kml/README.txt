collective.geo.kml
=================

Overview
--------
collective.geo.kml provides the necessary javascript to integrate a kml document in an openlayers layer.
It builds a kml file for Folder and Collection objects.
Some kml properties can be set at site level.

Test
----
We have a generic (georeferenceable) Document and set some geographical data with collective.geo.geographer package

    >>> folder = layer['portal']['folder']
    >>> document = folder['doc']
    >>> from collective.geo.geographer.interfaces import IWriteGeoreferenced
    >>> geo = IWriteGeoreferenced(document)
    >>> geo.setGeoInterface('Point', (-100, 40))
    >>> document.reindexObject(idxs=['zgeo_geometry'])

Set some extra metadata on the document so we can check for those

    >>> document.setSubject(['Mapping', 'Geography', 'Google'])
    >>> document.creators = ('David', 'John', 'Bob')
    >>> document.rights = 'Some sort of copyright notice'

Set the dates for the content so they are consistent and can be tested

    >>> import DateTime
    >>> testDate = DateTime.DateTime('2010/01/01 09:00:00.000 '+DateTime.DateTime().timezone())
    >>> document.creation_date = testDate
    >>> document.effective_date = testDate
    >>> document.modification_date = testDate
    >>> document.reindexObject()
    >>> import transaction
    >>> transaction.commit()

The folder that contains our document have a kml-document view

    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import TEST_USER_NAME
    >>> from plone.app.testing import TEST_USER_PASSWORD
    >>> browser = Browser(layer['app'])
    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))
    >>> browser.open("%s/@@kml-document" % folder.absolute_url())

    >>> print browser.contents
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
            <Style id="defaultStyle">
              <IconStyle>
                <scale>0.7</scale>
               <Icon>
                <href>http://nohost/plone/img/marker.png</href>
               </Icon>
               <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />
              </IconStyle>
              <LineStyle>
               <color>3c0000ff</color>
               <width>2.0</width>
              </LineStyle>
              <PolyStyle>
                <color>3c0000ff</color>
              </PolyStyle>
              <BalloonStyle>
                <text><![CDATA[<h2>$[name]</h2>$[description]]]></text>
              </BalloonStyle>
            </Style>
    ...
      <Placemark>
        <name>Test document</name>
        <atom:author>
           <atom:name>David</atom:name>
        </atom:author>
        <atom:link href="http://nohost/plone/folder/doc"/>
    ...
            <p>A test document</p>
    ...
                    <p class="placemark-url">
                        <a href="http://nohost/plone/folder/doc">See the original resource</a>
                    </p>
    ...
            <styleUrl>#defaultStyle</styleUrl>
    ...
          <coordinates>-100.000000,40.000000,0.0</coordinates>
    ...
      </Placemark>
    ...
    </kml>
    <BLANKLINE>

we can change some properties of kml document with IGeoKmlSettings utility
    >>> from zope.component import getUtility
    >>> from plone.registry.interfaces import IRegistry
    >>> registry = getUtility(IRegistry)
    >>> from collective.geo.settings.interfaces import IGeoFeatureStyle
    >>> settings = registry.forInterface(IGeoFeatureStyle)
    >>> settings.linecolor = u'33DD223C'
    >>> settings.linewidth = 3.0
    >>> settings.polygoncolor = u'FFBD003C'
    >>> settings.marker_image = u'string:${portal_url}/img/marker-blue.png'
    >>> settings.marker_image_size = 1.0
    >>> settings.display_properties = ['listCreators', 'Type', 'Subject',
    ...     'Contributors']
    >>> transaction.commit()

    >>> browser.open("%s/@@kml-document" % folder.absolute_url())
    >>> print browser.contents
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
                    <dl class="placemark-properties">
    <BLANKLINE>
                        <dt>Creators</dt>
                        <dd>David John Bob</dd>
    <BLANKLINE>
                        <dt>Type</dt>
                        <dd>Page</dd>
    <BLANKLINE>
                        <dt>Subject</dt>
                        <dd>Mapping Geography Google</dd>
    <BLANKLINE>
                        <dt>Contributors</dt>
                        <dd></dd>
    <BLANKLINE>
                    </dl>
    ...
    </kml>


We can also change properties on a per-document registering a proper adapter to annotate the setting in a content type
see:
 collective.geo.contentlocations.geostylemanager

    >>> from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
    >>> from collective.geo.geographer.interfaces import IGeoreferenceable
    >>> from zope.component import provideAdapter
    >>> from collective.geo.kml.testing import CustomStyleManager
    >>> provideAdapter(CustomStyleManager, (IGeoreferenceable,), IGeoCustomFeatureStyle)
    >>> custom_styles = IGeoFeatureStyle(document)
    >>> custom_styles.linewidth
    2.0

    >>> custom_styles.polygoncolor
    u'FEDCBA3C'

    >>> browser.open("%s/@@kml-document" % folder.absolute_url())
    >>> print browser.contents
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
            <Style id="defaultStyle">
              <IconStyle>
                <scale>1.0</scale>
               <Icon>
                <href>http://nohost/plone/img/marker-blue.png</href>
               </Icon>
               <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />
              </IconStyle>
    ...
            <Point>
              <coordinates>-100.000000,40.000000,0.0</coordinates>
            </Point>
    ...
    </kml>
    <BLANKLINE>



Let's try a LineString instead to see it's custom styles

    >>> geo.setGeoInterface('LineString', ((0.111,0.222),) )
    >>> document.reindexObject(idxs=['zgeo_geometry'])
    >>> transaction.commit()

    >>> browser.open("%s/@@kml-document" % folder.absolute_url())
    >>> print browser.contents
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
    <LineStyle>
      <color>3CBADCFE</color>
      <width>2.0</width>
    </LineStyle>
    ...
    <LineString>
      <coordinates>0.111000,0.222000,0.0</coordinates>
    </LineString>
    ...
    </kml>
    <BLANKLINE>


Finally, let's try a Polygon to see it's custom styles

    >>> geo.setGeoInterface('Polygon', (((0.111,0.222),(0.222,0.222),(0.222,0.111),(0.111,0.111)),) )
    >>> document.reindexObject(idxs=['zgeo_geometry'])
    >>> transaction.commit()

    >>> browser.open("%s/@@kml-document" % folder.absolute_url())
    >>> print browser.contents
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
      <PolyStyle>
        <color>3CBADCFE</color>
      </PolyStyle>
    ...
    <Polygon>
    <outerBoundaryIs>
      <LinearRing>
        <coordinates>0.111000,0.222000,0.0 0.222000,0.222000,0.0 0.222000,0.111000,0.0 0.111000,0.111000,0.0</coordinates>
      </LinearRing>
    </outerBoundaryIs>
    </Polygon>
    ...
    </kml>
    <BLANKLINE>
