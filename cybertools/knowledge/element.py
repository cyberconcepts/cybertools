# cybertools.knowledge.element

""" Represent knowledge elements and their interrelations.
"""

from zope.interface import implementer
from cybertools.knowledge.interfaces import IKnowledgeElement


@implementer(IKnowledgeElement)
class KnowledgeElement(object):

    def __init__(self):
        self._parent = None
        self._dependencies = {}
        # backlinks:
        self._children = set()
        self._dependents = set()
        self._knowers = set()
        self._providers = set()

    def setParent(self, obj):
        old = self._parent
        if old is not None and old != obj:
            del old._children[self]
        if obj is not None and old != obj:
            obj._children.add(self)
        self._parent = obj
    def getParent(self): return self._parent
    parent = property(getParent, setParent)

    def getDependencies(self):
        return self._dependencies

    def dependsOn(self, obj):
        self._dependencies[obj] = True
        obj._dependents.add(self)

    def removeDependency(self, obj):
        del self._dependencies[obj]
        del obj._dependents[self]

    def getDependents(self):
        return self._dependents

    def getKnowers(self):
        return self._knowers

    def getProviders(self):
        return tuple(self._providers)

