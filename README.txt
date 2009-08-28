Introduction
============

collective.geo.kml provides KML views of georeferenced objects, allowing Plone containers and collections to be visualized in Google Earth.

It provides a map view to Plone Folder and Topic content types to display kml data.

Requirements
------------
* plone >= 3.2.1
* collective.geo.contentlocations
* zgeo.plone.kml

Installation
============
Just a simple easy_install collective.geo.kml is enough.

Alternatively, buildout users can install collective.geo.kml as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            zope.i18n>=3.4
            collective.geo.kml
        ...
        [instance]
        ...
        zcml = 
            collective.geo.kml


Contributors
============

* Sean Gillies 
* Giorgio Borelli
* Silvio Tomatis

