#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Basic implementation of the elements used for the intermediate format for export
and import of objects.

$Id$
"""

import os
from zope import component
from zope.cachedescriptors.property import Lazy
from zope.dottedname.resolve import resolve
from zope.interface import Interface, implements
from zope.traversing.api import getName, traverse

from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import ISchemaFactory
from cybertools.external.interfaces import IElement


class Element(dict):

    implements(IElement)

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
