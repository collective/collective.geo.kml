from zope.schema import vocabulary

GLOBALS = globals()

PROJECTNAME = "collective.geo.kml"

#SimpleTerm are specified as (value, token, title).  Default action on a None token defaults to str(title).
DISPLAY_VOCABULARY = vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(*value) for value in [
                       ('id', None, 'ID'),
                       ('Type', None, 'Type'),
                       ('Subject', None, 'Subject'),
                       ('getLocation', None, 'Content Location'),
                       ('ModificationDate', None, 'Last Modified Date'),
                       ('CreationDate', None, 'Creation Date'),
                       ('EffectiveDate', None, 'Effective Date'),
                       ('ExpirationDate', None, 'Expiration Date'),
                       ('listCreators', None, 'Creators'),
                       ('Contributors', None, 'Contributors'),
                       ('Rights', None, 'Rights Statement'),
                        ]
                     ])

#Define those terms that are structures, rather than single variables
DISPLAY_PROPERTY_STRUCTURES = ['Subject', 'listCreators', 'Contributors']
