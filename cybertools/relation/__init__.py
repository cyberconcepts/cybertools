# cybertools.relation

""" The relation package provides all you need for setting up dyadic and
triadic relations.
"""

from persistent import Persistent
from zope.interface import implementer
from cybertools.relation.interfaces import IPredicate
from cybertools.relation.interfaces import IRelation, IDyadicRelation, ITriadicRelation
from cybertools.relation.interfaces import IRelatable


@implementer(IPredicate, IRelation)
class Relation(Persistent):

    order = 0
    relevance = 1.0
    fallback = None

    @classmethod
    def getPredicateName(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    @property
    def ident(self):
        return self.getPredicateName()

    def validate(self, registry=None):
        return True

    def checkRelatable(self, *objects):
        for obj in objects:
            if obj is not None and not IRelatable.providedBy(obj):
                raise(ValueError, 'Objects to be used in relations '
                        'must provide the IRelatable interface.')


@implementer(IDyadicRelation)
class DyadicRelation(Relation):

    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.checkRelatable(first, second)


@implementer(ITriadicRelation)
class TriadicRelation(Relation):

    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
        self.checkRelatable(first, second, third)

