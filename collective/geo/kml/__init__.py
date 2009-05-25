from zope.i18nmessageid import MessageFactory
from collective.geo.kml import config

GeoKmlMessageFactory = MessageFactory(config.PROJECTNAME)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
