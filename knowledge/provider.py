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
Knowledge providers provide knowledge.

$Id$
"""

from zope.interface import implements
from cybertools.knowledge.interfaces import IKnowledgeProvider


class KnowledgeProvider(object):

    implements(IKnowledgeProvider)
    
    def __init__(self):
        self._providedKnowledge = {}

    def getProvidedKnowledge(self):
        return self._providedKnowledge

    def provides(self, obj):
        self._providedKnowledge[obj] = True
        obj._providers.add(self)

    def removeProvidedKnowledge(self, obj):
        del self._providedKnowledge[obj]
        del obj._providers[self]

