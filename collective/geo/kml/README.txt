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
        <Placemark>
          <name>Test document</name>
          <description>
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <p><strong>URL:</strong> 
                  <a href="http://localhost/plone/Members/test_user_1_/test-document">Item URL
                  </a>
                </p>
                <p><strong>Type:</strong> <span>Document</span></p>
                <p><strong>Last Modified:</strong> <span>Jan 01, 2010 09:00 AM</span></p>
                <p><strong>Creation Date:</strong> <span>Jan 01, 2010 09:00 AM</span></p>
    <BLANKLINE>
              </div>
            ]]>
          </description>
          <styleUrl>#defaultStyle</styleUrl>
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
        <Placemark>
          <name>Test document</name>
          <description>
            <![CDATA[
              <div>
    <BLANKLINE>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas malesuada, sapien non tincidunt semper, elit tortor varius neque, non fringilla dui nisi ac lacus. Aliquam erat volutpat. Etiam lobortis pharetra eleifend</p>
                <p><strong>URL:</strong> 
                  <a href="http://localhost/plone/Members/test_user_1_/test-document">Item URL
                  </a>
                </p>
                <p><strong>Type:</strong> <span>Document</span></p>
                <p><strong>Last Modified:</strong> <span>Jan 01, 2010 09:00 AM</span></p>
                <p><strong>Creation Date:</strong> <span>Jan 01, 2010 09:00 AM</span></p>
    <BLANKLINE>
              </div>
            ]]>
          </description>
          <styleUrl>#defaultStyle</styleUrl>
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

