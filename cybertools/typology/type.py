# cybertools.typology.type

""" Abstract base classes for type management.
"""

from zope.interface import implementer
from cybertools.typology.interfaces import IType, ITypeManager


@implementer(IType)
class BaseType(object):

    def __init__(self, context):
        self.context = context

    def __eq__(self, other):
        return IType.providedBy(other) and self.token == other.token

    title = u'BaseType'

    @property
    def token(self):
        return str(self.title.lower().replace(' ', '_'))

    @property
    def tokenForSearch(self): return self.token

    qualifiers = None
    typeInterface = None
    factory = None
    defaultContainer = None
    viewName = ''
    typeProvider = None

    @property
    def options(self):
        return []


@implementer(ITypeManager)
class TypeManager(object):

    @property
    def types(self):
        return (BaseType(None),)

    def listTypes(self, **criteria):
        return self.types

    def getType(self, token):
        for t in self.types:
            if t.token == token:
                return t
        raise ValueError('Unrecognized token: ' + token)

