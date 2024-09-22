# cybertools.external.element

""" Basic implementation of the elements used for the intermediate format for export
and import of objects.
"""

import os
from zope import component
from zope.cachedescriptors.property import Lazy
from zope.dottedname.resolve import resolve
from zope.interface import Interface, implementer
from zope.traversing.api import getName, traverse

from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import ISchemaFactory
from cybertools.external.interfaces import IElement


@implementer(IElement)
class Element(dict):

    encoding = 'UTF-8'
    type = ''
    identifierName = ''
    object = None
    parent = None
    subElements = None
    parentType = ''
    order = 0

    @property
    def identifier(self):
        id = self.get(self.identifierName)
        return id

    def __getitem__(self, key):
        if isinstance(key, Element):
            key = (key,)
        if isinstance(key, tuple):
            for item in key:
                item.parent = self
                self.add(item)
            return key
        return super(Element, self).__getitem__(key)

    def processExport(self, extractor):
        pass

    def add(self, element):
        if self.subElements is None:
            self.subElements = []
        self.subElements.append(element)
        element.parent = self

    def setParent(self, elementsMapping, allElements=None):
        pt = self.parentType
        if pt:
            pCurr = elementsMapping.get(pt)
            if pCurr is not None:
                if allElements and pCurr.identifier:
                    parent = allElements.get(pt, {}).get(pCurr.identifier)
                else:
                    parent = pCurr
                if parent is not None:
                    parent.add(self)


    def execute(self, loader):
        pass

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, dict.__repr__(self))
