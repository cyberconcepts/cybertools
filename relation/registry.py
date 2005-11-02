#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
Implementation of the utilities needed for the relations package.

$Id$
"""

from zope.interface import implements
from zope.app import zapi
from persistent import Persistent
from zope.app.container.contained import Contained

from interfaces import IRelationsRegistry


class DummyRelationsRegistry(object):
    """ Dummy implementation for demonstration and test purposes.
    """

    implements(IRelationsRegistry)

    def __init__(self):
        self.relations = []

    def register(self, relation):
        if relation not in self.relations:
            self.relations.append(relation)
    
    def unregister(self, relation):
        if relation in self.relations:
            self.relations.remove(relation)
    
    def query(self, **kw):
        result = []
        for r in self.relations:
            hit = True
            for k in kw:
                if k == 'relationship':
                    if kw[k] != r.__class__:
                        hit = False
                        break
                elif not hasattr(r, k) or getattr(r, k) != kw[k]:
                    hit = False
                    break
            if hit:
                result.append(r)
        return result


class RelationsRegistry(Persistent, Contained):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    implements(IRelationsRegistry)

    def register(self, relation):
        pass
    
    def unregister(self, relation):
        pass
    
    def query(self, **kw):
        result = []
        return result

            