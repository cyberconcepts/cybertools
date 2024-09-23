# cybertools.typology.example.person

""" Example classes for the cybertools.typology package. 

These use the cybertools.organize package
"""

from zope.component import adapts
from zope.interface import implementer
from cybertools.organize.interfaces import IPerson
from cybertools.typology.interfaces import IType, ITypeManager
from cybertools.typology.type import BaseType, TypeManager


# interfaces

class IAgeGroup(IType):
    """ A type interface for discerning childs and adults.
    """


class IAgeGroupManager(ITypeManager):
    """ A type manager managing age groups.
    """


# implementations

@implementer(IAgeGroup)
class AgeGroup(BaseType):

    adapts(IPerson)

    # IType attributes

    @property
    def title(self):
        return self.isChild and u'Child' or u'Adult'

    @property
    def token(self): return 'organize.person.agegroup.' + str(self.title.lower())

    # helpers

    @property
    def isChild(self):
        return self.context.age < 18.0


class AgeGroupTypeInfo(AgeGroup):
    """ Age group type info object with fixed (not computed) isChild property.
    """

    isChild = None

    def __init__(self, isChild):
        self.isChild = isChild


@implementer(IAgeGroupManager)
class AgeGroupManager(TypeManager):

    @property
    def types(self):
        return tuple([AgeGroupTypeInfo(flag) for flag in (True, False)])

