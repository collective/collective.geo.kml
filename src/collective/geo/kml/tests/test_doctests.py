import unittest2 as unittest
import doctest
import transaction

from plone.testing import layered
from ..testing import CGEO_KML_FUNCTIONAL

from zope.interface import alsoProvides
from zope.component.hooks import getSite
from zope.component import getGlobalSiteManager


from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IWriteGeoreferenced
from ..testing import CustomStyleManager


def set_default_styles():
    from zope.component import getUtility
    from plone.registry.interfaces import IRegistry
    registry = getUtility(IRegistry)
    from collective.geo.settings.interfaces import IGeoFeatureStyle
    settings = registry.forInterface(IGeoFeatureStyle)
    settings.linecolor = u'ff00003c'
    settings.linewidth = 2.0
    settings.polygoncolor = u'ff00003c'
    settings.marker_image = u'string:${portal_url}/img/marker.png'
    settings.marker_image_size = 0.7
    settings.display_properties = ['Title', 'Description']


def create_base_content(portal):
    setRoles(portal, TEST_USER_ID, ['Manager'])
    _id = portal.invokeFactory(
        'Folder', 'folder',
        title='Folder',
        description="Collective geo test container"
    )
    folder = portal.get(_id)

    # set default view for folder
    folder.setLayout('kml-openlayers')

    behavior = 'collective.geo.behaviour.interfaces.ICoordinates'
    fti = portal.portal_types.get('Document')
    behaviors = list(fti.behaviors)
    behaviors.append(behavior)
    behaviors = tuple(behaviors)
    fti._updateProperty('behaviors', behaviors)

    # create topic
    # topic_id = folder.invokeFactory('Topic', 'topic', title="Test Topic")
    # topic = folder[topic_id]

    # c = topic.addCriterion('getId', 'ATSimpleStringCriterion')
    # c.setValue('doc')

    # create collection
    collection_id = folder.invokeFactory(
        'Collection',
        'collection',
        title="Test Collection")
    collection = folder[collection_id]
    query = [{
        'i': 'getId',
        'o': 'plone.app.querystring.operation.string.is',
        'v': 'doc'
    }]
    collection.setQuery(query)

    # create document and georeference it
    doc_id = folder.invokeFactory(
        'Document',
        'doc',
        title='Test document',
        description='A test document')

    doc = folder[doc_id]
    # alsoProvides(doc, IGeoreferenceable)

    geo = IWriteGeoreferenced(doc)
    geo.setGeoInterface('Point', (-105, 40))
    doc.reindexObject(idxs=['zgeo_geometry'])

    setRoles(portal, TEST_USER_ID, ['Member'])


def remove_base_contents(portal):
    setRoles(portal, TEST_USER_ID, ['Manager'])
    portal.manage_delObjects('folder')
    setRoles(portal, TEST_USER_ID, ['Member'])


def setUp(self):  # pylint: disable=W0613
    portal = getSite()
    create_base_content(portal)
    transaction.commit()


def tearDown(self):  # pylint: disable=W0613
    portal = getSite()
    remove_base_contents(portal)
    set_default_styles()

    gsm = getGlobalSiteManager()
    gsm.unregisterAdapter(CustomStyleManager, (IGeoreferenceable, ))

    transaction.commit()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([

        layered(
            doctest.DocFileSuite(
                'README.txt',
                package='collective.geo.kml',
                setUp=setUp,
                tearDown=tearDown,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                            doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        layered(
            doctest.DocFileSuite(
                'browser/kmlopenlayersview.txt',
                package='collective.geo.kml',
                setUp=setUp,
                tearDown=tearDown,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        layered(
            doctest.DocFileSuite(
                'kml-docs.txt',
                package='collective.geo.kml.tests',
                setUp=setUp,
                tearDown=tearDown,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

        # layered(
        #     doctest.DocFileSuite(
        #         'kml-docs-old-topic.txt',
        #         package='collective.geo.kml.tests',
        #         setUp=setUp,
        #         tearDown=tearDown,
        #         optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
        #                 doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        #     ),
        #     layer=CGEO_KML_FUNCTIONAL
        # ),

        layered(
            doctest.DocFileSuite(
                'folder-kml.txt',
                package='collective.geo.kml.tests',
                setUp=setUp,
                tearDown=tearDown,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                    doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_KML_FUNCTIONAL
        ),

    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
