collective.geo.kml
=================

Overview
--------
collective.geo.kml provides the necessary javascript to integrate a kml document in an opelayers layer.
It build a kml file for Folder and Topic objects. 
Some kml properties can be set at site level.

Test
----
We have a generic (georeferenceable) Document and set some geographical data with collective.geo.geographer package

    >>> document = self.folder['test-document']
    >>> from collective.geo.geographer.interfaces import IWriteGeoreferenced
    >>> geo = IWriteGeoreferenced(document)
    >>> geo.setGeoInterface('Point', (-100, 40))

Set some extra metadata on the document so we can check for those

    >>> document.setSubject(['Mapping', 'Geography', 'Google'])
    >>> document.setLocation('Somewhere on Earth')
    >>> document.setCreators(['David', 'John', 'Bob'])
    >>> document.setRights('Some sort of copyright notice')
    >>> document.reindexObject()

Set the dates for the content so they are consistent and can be tested

    >>> import DateTime
    >>> testDate = DateTime.DateTime('2010/01/01 09:00:00.000 '+DateTime.DateTime().timezone())
    >>> document.setCreationDate(testDate)
    >>> document.setEffectiveDate(testDate)
    >>> document.setModificationDate(testDate)
    >>> document.indexObject()

Folder that contain our document have a kml-document view
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
            <Style id="defaultStyle">
              <IconStyle>
                <scale>0.7</scale>
               <Icon>
                <href>http://localhost/plone/img/marker.png</href>
               </Icon>
               <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
              </IconStyle>
              <LineStyle>
               <color>3c0000ff</color>
               <width>2.0</width>
              </LineStyle>
              <PolyStyle>
                <color>3c0000ff</color>
              </PolyStyle>
            </Style>
    ...
          <Placemark>
            <name>Test document</name>
            <atom:author>
               <atom:name>David</atom:name>
            </atom:author>
            <atom:link href="http://localhost/plone/Members/test_user_1_/test-document"/>
    ...
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
    ...
                        <dt>Title</dt>
                        <dd>Test document</dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Description</dt>
                        <dd>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</dd>
    ...
                <p class="placemark-url">
                    <a href="http://localhost/plone/Members/test_user_1_/test-document">See the original resource</a>
                </p>
    ...
                <styleUrl>#defaultStyle</styleUrl>
    ...
              <coordinates>-100.000000,40.000000,0.0</coordinates>
            </Point>
    ...
    </kml>

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
    ...                                'CreationDate', 'Contributors', 'getLocation']

    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
                    <dl class="placemark-properties">
    <BLANKLINE>
                        <dt>Creators</dt>
                        <dd>David John Bob</dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Type</dt>
                        <dd>Page</dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Subject</dt>
                        <dd>Mapping Geography Google</dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Creation Date</dt>
                        <dd>Jan 01, 2010 ...</dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Contributors</dt>
                        <dd></dd>
    <BLANKLINE>
    <BLANKLINE>
                        <dt>Content Location</dt>
                        <dd>Somewhere on Earth</dd>
    <BLANKLINE>
                    </dl>
    ...
    </kml>


We can also change properties on a per-document registering a proper adapter to annotate the setting in a content type
see: 
 collective.geo.contentlocations.geostylemanager
 collective.geo.kml.tests.base

        >>> from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
        >>> from collective.geo.geographer.interfaces import IGeoreferenceable
        >>> from zope.component import provideAdapter
        >>> from collective.geo.kml.tests.base import CustomStyleManager
        >>> provideAdapter(CustomStyleManager, (IGeoreferenceable,), IGeoCustomFeatureStyle)
        >>> custom_styles = IGeoFeatureStyle(document)
        >>> custom_styles.geostyles.get('linewidth')
        2.0

        >>> custom_styles.geostyles.get('polygoncolor')
        u'FEDCBA3C'

Now that we're using a custom style, we should see that reflected in our KML
document view.
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ...
    <Style>
      <IconStyle>
        <scale>1.0</scale>
       <Icon>
        <href>http://localhost/plone/img/marker.png</href>
       </Icon>
       <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
      </IconStyle>
    ...
    <Point>
      <coordinates>-100.000000,40.000000,0.0</coordinates>
    </Point>
    ...
    </kml>

Let's try a LineString instead to see it's custom styles

    >>> geo.setGeoInterface('LineString', ((0.111,0.222),) )

We can check the output now that we're using a custom-styled LineString
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
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

Finally, let's try a Polygon to see it's custom styles

    >>> geo.setGeoInterface('Polygon', (((0.111,0.222),(0.222,0.222),(0.222,0.111),(0.111,0.111)),) )
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
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
