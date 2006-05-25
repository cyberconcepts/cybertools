#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Represent knowledge elements and their interrelations.

$Id$
"""

from zope.interface import implements
from cybertools.knowledge.interfaces import IKnowledgeElement


class KnowledgeElement(object):

    implements(IKnowledgeElement)
    
    def __init__(self):
        self._parent = None
        self._dependencies = {}
        # backlinks:
        self._children = set()
        self._dependents = set()
        self._knowers = set()
        self._requiringPositions = set()
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

