Introduction
============

collective.geo.kml overrides kml-document provided by "zgeo.plone.kml" package to integrate some additional options.

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

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
