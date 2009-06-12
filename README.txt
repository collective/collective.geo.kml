Introduction
============

collective.geo.kml override kml-document view of zgeo.plone.kml for integrate some additional options to that view
and provide a map view for its.

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


Usage
=====

* Install this product from the Plone control panel.
* Add some contents with coordinates value on your portal (see collective.geo.contentlocations for more informations) in a folder
* Select "openlayers view" item in the view menu
* You should have changed the view of this folder and view a map that include geographical information about folder contents.

You have the same view for the collection content type.


