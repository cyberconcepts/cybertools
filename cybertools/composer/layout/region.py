# cybertools.composer.layout.region

""" Region implementation.
"""

from zope.interface import implementer

from cybertools.composer.layout.interfaces import IRegion
from cybertools.util.jeep import Jeep


@implementer(IRegion)
class Region(object):

    allowedLayoutCategories = None

    def __init__(self, name):
        self.name = name
        self.layouts = Jeep()
