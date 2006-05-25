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
Manage objects (people) who know something.

$Id$
"""

from zope.interface import implements
from cybertools.knowledge.interfaces import IKnowing


class Knowing(object):

    implements(IKnowing)

    def __init__(self):
        self._knowledge = {}

    def getKnowledge(self):
        return self._knowledge

    def knows(self, obj):
        self._knowledge[obj] = True
        obj._knowers.add(self)

    def removeKnowledge(self, obj):
        del self._knowledge[obj]
        del obj._knowers[self]

    def getMissingKnowledge(self, position):
        # to be done
        return tuple(position.getRequirements())

    def getProvidersNeeded(self, position):
        return ((k, k.getProviders())
                    for k in self.getMissingKnowledge(position))


