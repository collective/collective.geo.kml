Introduction
============

collective.geo.kml provides `KML`_ views for georeferenced objects, allowing Plone containers and collections to be visualized in `Google Earth`_.

It also provides a map view to Plone Folder and Topic content types to display kml data.

.. image:: https://secure.travis-ci.org/collective/collective.geo.kml.png
    :target: http://travis-ci.org/collective/collective.geo.kml

Found a bug? Please, use the `issue tracker`_.


.. contents:: Table of contents


Requirements
============
* `Plone`_ >= 4.0
* `collective.geo.geographer`_
* `collective.geo.mapwidget`_


Installation
============
You can install collective.geo.kml as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs =
            collective.geo.kml
        ...


Contributors
============

* Sean Gillies
* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey - davidjb
* Christian Ledermann - nan
* Rob Gietema - robgietema
* Leonardo J. Caballero G - macagua


.. _Plone: http://plone.org
.. _KML: http://en.wikipedia.org/wiki/Keyhole_Markup_Language
.. _Google Earth: http://www.google.com/earth/index.html
.. _collective.geo.mapwidget: http://pypi.python.org/pypi/collective.geo.mapwidget
.. _collective.geo.geographer: http://pypi.python.org/pypi/collective.geo.geographer
.. _issue tracker: https://github.com/collective/collective.geo.bundle/issues
