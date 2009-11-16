collective.geo.kml
=================

Overview
--------
collective.geo.kml provides the necessary javascript to integrate a kml document in an opelayers layer.
It uses zgeo.plone.kml to build a kml file for Folder and Topic objects.
Some kml properties can be set at site level.

Test
----
We have a generic Document and set some geographical data with IGeoManager from collective.geo.contentlocations package

    >>> document = self.folder['test-document']
    >>> from collective.geo.contentlocations.interfaces import IGeoManager
    >>> geo = IGeoManager(document)
    >>> geo.setCoordinates('Point', (45, 7))

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

Folder that contain our document have a kml-document view provided by zgeo.plone.kml
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
    <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <BLANKLINE>
      <Document>
        <Style id="defaultStyle">
          <IconStyle>
            <scale>0.7</scale>
            <Icon>
                <href>http://localhost/plone/img/marker.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
          </IconStyle>
          <LineStyle>
            <color>FF0000FF</color>
            <width>2.0</width>
          </LineStyle>
          <PolyStyle>
            <color>3C0000FF</color>
          </PolyStyle>
        </Style>
        <name></name>
        <visibility>1</visibility>
        <open>0</open>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <Placemark>
            <name>
            <![CDATA[
             <a href="http://localhost/plone/Members/test_user_1_/test-document">Test document</a> 
            ]]>
            </name>
          <description>
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <dl>
    <BLANKLINE>
                  <dt>ID</dt>
                  <dd>test-document</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Type</dt>
                  <dd>Page</dd>
    <BLANKLINE>
                </dl>
              </div>
            ]]>
            </description>
    <BLANKLINE>
            <styleUrl>#defaultStyle</styleUrl>
    <BLANKLINE>
    <BLANKLINE>
            <Point>
              <coordinates>45.000000,7.000000,0.0</coordinates>
            </Point>
    <BLANKLINE>
    <BLANKLINE>
        </Placemark>
    <BLANKLINE>
      </Document>
    </kml>
    <BLANKLINE>

we can change some properties of kml document with IGeoKmlSettings utility
    >>> from zope.component import getUtility
    >>> from collective.geo.kml.interfaces import IGeoKmlSettings
    >>> settings = getUtility(IGeoKmlSettings)
    >>> settings.linecolor = '#33DD22'
    >>> settings.linewidth = 3.0
    >>> settings.polygoncolor = '#FFBD00'
    >>> settings.marker_image = 'img/marker-blue.png'
    >>> settings.marker_image_size = 1.0
    >>> settings.display_properties = ['listCreators', 'Type', 'Subject',
    ... 'ExpirationDate', 'Contributors', 'Rights']
    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
        <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <BLANKLINE>
      <Document>
        <Style id="defaultStyle">
          <IconStyle>
            <scale>1.0</scale>
            <Icon>
                <href>http://localhost/plone/img/marker-blue.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
          </IconStyle>
          <LineStyle>
            <color>FF22DD33</color>
            <width>3.0</width>
          </LineStyle>
          <PolyStyle>
            <color>3C00BDFF</color>
          </PolyStyle>
        </Style>
        <name></name>
        <visibility>1</visibility>
        <open>0</open>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <Placemark>
            <name>
            <![CDATA[
             <a href="http://localhost/plone/Members/test_user_1_/test-document">Test document</a> 
            ]]>
            </name>
            <description> 
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <dl>
    <BLANKLINE>
                  <dt>Creators</dt>
                  <dd>David, John, Bob</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Type</dt>
                  <dd>Page</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Subject</dt>
                  <dd>Mapping, Geography, Google</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Expiration Date</dt>
                  <dd>None</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Contributors</dt>
                  <dd>None</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Rights Statement</dt>
                  <dd>Some sort of copyright notice</dd>
    <BLANKLINE>
                </dl>
              </div>
            ]]>
            </description>
    <BLANKLINE>
            <styleUrl>#defaultStyle</styleUrl>
    <BLANKLINE>
    <BLANKLINE>
            <Point>
              <coordinates>45.000000,7.000000,0.0</coordinates>
            </Point>
    <BLANKLINE>
    <BLANKLINE>
          </Placemark>
    <BLANKLINE>
      </Document>
    </kml>
    <BLANKLINE>


We can also change properties on a per-document basis with the IGeoContentKmlSettings utility
    >>> from collective.geo.kml.interfaces import IGeoContentKmlSettings
    >>> kml_settings = IGeoContentKmlSettings(document)
    >>> kml_settings.initialiseStyles(document)

We can obtain a given KML property by the 'get' method.
These will just be the the default values at present.
    >>> styles = kml_settings.getStyles(document)
    >>> styles['use_custom_style']
    False
    >>> styles['marker_image']
    u'img/marker.png'

We typically use the 'get' method to access our properties
    >>> kml_settings.get('use_custom_style')
    False
    >>> kml_settings.get('linewidth')
    2.0

We can configure settings through GeoContentKmlSettings using 'set'

    >>> kml_settings.set('linecolor', '#ABCDEF')
    >>> kml_settings.get('linecolor')
    '#ABCDEF'

    >>> kml_settings.set('linewidth', 1.0)
    >>> kml_settings.get('linewidth')
    1.0

    >>> kml_settings.set('polygoncolor', '#FEDCBA')
    >>> kml_settings.get('polygoncolor')
    '#FEDCBA'

    >>> kml_settings.set('marker_image', 'marker-blue.png')
    >>> kml_settings.get('marker_image')
    'marker-blue.png'

    >>> kml_settings.set('marker_image_size', 1.0)
    >>> kml_settings.get('marker_image_size')
    1.0

Set some custom display properties to watch the change.

    >>> kml_settings.set('display_properties', ['getLocation', 'Type', 'EffectiveDate', 'ModificationDate'])
    >>> kml_settings.get('display_properties')
    ['getLocation', 'Type', 'EffectiveDate', 'ModificationDate']

Make sure we're using the custom styles, or else we won't see anything
different.

    >>> kml_settings.set('use_custom_style', True)
    >>> kml_settings.get('use_custom_style')
    True

Now that we're using a custom style, we should see that reflected in our KML
document view.  The styleUrl tag disappears and we see the custom style
instead.  Note the defaultStyle identifier is still present as this can be
used by other non-customised placemarks.

    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
        <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <BLANKLINE>
      <Document>
        <Style id="defaultStyle">
          <IconStyle>
            <scale>1.0</scale>
            <Icon>
                <href>http://localhost/plone/img/marker-blue.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
          </IconStyle>
          <LineStyle>
            <color>FF22DD33</color>
            <width>3.0</width>
          </LineStyle>
          <PolyStyle>
            <color>3C00BDFF</color>
          </PolyStyle>
        </Style>
        <name></name>
        <visibility>1</visibility>
        <open>0</open>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <Placemark>
            <name>
            <![CDATA[
             <a href="http://localhost/plone/Members/test_user_1_/test-document">Test document</a> 
            ]]>
            </name>
            <description> 
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <dl>
    <BLANKLINE>
                  <dt>Content Location</dt>
                  <dd>Somewhere on Earth</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Type</dt>
                  <dd>Page</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Effective Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Last Modified Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
                </dl>
              </div>
            ]]>
            </description>
    <BLANKLINE>
    <BLANKLINE>
            <Style>
              <IconStyle>
                  <scale>1.0</scale>
                  <Icon>
                    <href>marker-blue.png</href>
                  </Icon>
                  <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
              </IconStyle>
    <BLANKLINE>
    <BLANKLINE>
            </Style>
    <BLANKLINE>
            <Point>
              <coordinates>45.000000,7.000000,0.0</coordinates>
            </Point>
    <BLANKLINE>
    <BLANKLINE>
          </Placemark>
    <BLANKLINE>
      </Document>
    </kml>
    <BLANKLINE>

Let's try a LineString instead to see it's custom styles

>>> geo.setCoordinates('LineString', ((0.111,0.222),) )

Set the dates for the content (again) so they are consistent and can be tested

    >>> import DateTime
    >>> testDate = DateTime.DateTime('2010/01/01 09:00:00.000 '+DateTime.DateTime().timezone())
    >>> document.setCreationDate(testDate)
    >>> document.setEffectiveDate(testDate)
    >>> document.setModificationDate(testDate)
    >>> document.indexObject()

We can check the output now that we're using a custom-styled LineString

    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
        <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <BLANKLINE>
      <Document>
        <Style id="defaultStyle">
          <IconStyle>
            <scale>1.0</scale>
            <Icon>
                <href>http://localhost/plone/img/marker-blue.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
          </IconStyle>
          <LineStyle>
            <color>FF22DD33</color>
            <width>3.0</width>
          </LineStyle>
          <PolyStyle>
            <color>3C00BDFF</color>
          </PolyStyle>
        </Style>
        <name></name>
        <visibility>1</visibility>
        <open>0</open>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <Placemark>
            <name>
            <![CDATA[
             <a href="http://localhost/plone/Members/test_user_1_/test-document">Test document</a> 
            ]]>
            </name>
            <description> 
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <dl>
    <BLANKLINE>
                  <dt>Content Location</dt>
                  <dd>Somewhere on Earth</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Type</dt>
                  <dd>Page</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Effective Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Last Modified Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
                </dl>
              </div>
            ]]>
            </description>
    <BLANKLINE>
    <BLANKLINE>
            <Style>
              <IconStyle>
                  <scale>1.0</scale>
                  <Icon>
                    <href>marker-blue.png</href>
                  </Icon>
                  <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
              </IconStyle>
              <LineStyle>
                  <color>FFEFCDAB</color>
                  <width>1.0</width>
              </LineStyle>
    <BLANKLINE>
            </Style>
    <BLANKLINE>
    <BLANKLINE>
            <LineString>
              <coordinates>0.111000,0.222000,0.0</coordinates>
            </LineString>
    <BLANKLINE>
          </Placemark>
    <BLANKLINE>
      </Document>
    </kml>
    <BLANKLINE>


Finally, let's try a Polygon to see it's custom styles

>>> geo.setCoordinates('Polygon', (((0.111,0.222),(0.222,0.222),(0.222,0.111),(0.111,0.111)),) )

Set the dates for the content (again) so they are consistent and can be tested

    >>> import DateTime
    >>> testDate = DateTime.DateTime('2010/01/01 09:00:00.000 '+DateTime.DateTime().timezone())
    >>> document.setCreationDate(testDate)
    >>> document.setEffectiveDate(testDate)
    >>> document.setModificationDate(testDate)
    >>> document.indexObject()

We can check the output now that we're using a custom-styled LineString

    >>> r = http(r"""
    ... GET /plone/Members/test_user_1_/@@kml-document HTTP/1.1
    ... Authorization: Basic %s:%s
    ... """ % (portal_owner, default_password), handle_errors=False)
    >>> print r.getBody()
        <?xml version="1.0" encoding="utf-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <BLANKLINE>
      <Document>
        <Style id="defaultStyle">
          <IconStyle>
            <scale>1.0</scale>
            <Icon>
                <href>http://localhost/plone/img/marker-blue.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
          </IconStyle>
          <LineStyle>
            <color>FF22DD33</color>
            <width>3.0</width>
          </LineStyle>
          <PolyStyle>
            <color>3C00BDFF</color>
          </PolyStyle>
        </Style>
        <name></name>
        <visibility>1</visibility>
        <open>0</open>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <Placemark>
            <name>
            <![CDATA[
             <a href="http://localhost/plone/Members/test_user_1_/test-document">Test document</a> 
            ]]>
            </name>
            <description> 
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <dl>
    <BLANKLINE>
                  <dt>Content Location</dt>
                  <dd>Somewhere on Earth</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Type</dt>
                  <dd>Page</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Effective Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
    <BLANKLINE>
                  <dt>Last Modified Date</dt>
                  <dd>2010-01-01 09:00:00</dd>
    <BLANKLINE>
                </dl>
              </div>
            ]]>
            </description>
    <BLANKLINE>
    <BLANKLINE>
            <Style>
              <IconStyle>
                  <scale>1.0</scale>
                  <Icon>
                    <href>marker-blue.png</href>
                  </Icon>
                  <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
              </IconStyle>
    <BLANKLINE>
              <PolyStyle>
                  <color>FFBADCFE</color>
              </PolyStyle>
            </Style>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
            <Polygon>
              <outerBoundaryIs>
                <LinearRing>
                  <coordinates>0.111000,0.222000,0.0 0.222000,0.222000,0.0 0.222000,0.111000,0.0 0.111000,0.111000,0.0</coordinates>
                </LinearRing>
              </outerBoundaryIs>
            </Polygon>
          </Placemark>
    <BLANKLINE>
      </Document>
    </kml>
    <BLANKLINE>
