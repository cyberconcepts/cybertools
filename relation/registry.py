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
from zope.app.catalog.catalog import Catalog
from zope.index.field import FieldIndex
from zope.app.intid.interfaces import IIntIds

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
                if ((k == 'relationship' and r.__class__ != kw[k])
                 or (k != 'relationship'
                        and (not hasattr(r, k) or getattr(r, k) != kw[k]))):
                    hit = False
                    break
            if hit:
                result.append(r)
        return result


class RelationsRegistry(Catalog):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    implements(IRelationsRegistry)

    def __init__(self, *args, **kwargs):
        Catalog.__init__(self, *args, **kwargs)
        self['relationship'] = FieldIndex()
        self['first'] = FieldIndex()
        self['second'] = FieldIndex()
        self['third'] = FieldIndex()

    def register(self, relation):
        relid = self._getUid(relation)
        for idx in self:
            index = self[idx]
            if idx == 'relationship':
                index.index_doc(relid, self._getRelationship(relation))
            else:
                target = getattr(relation, idx, None)
                index.index_doc(relid, target and self._getUid(target))
    
    def unregister(self, relation):
        self.unindex_doc(self._getUid(relation))
    
    def query(self, **kw):
        for k in kw:
            if k == 'relationship':
                quString = self._getClassString(kw[k])
            else:
                quString = self._getUid(kw[k])
            # set min, max
            kw[k] = (quString, quString)
        return self.searchResults(**kw)

    def _getUid(self, ob):
        return zapi.getUtility(IIntIds).getId(ob)

    def _getRelationship(self, relation):
        return self._getClassString(relation.__class__)

    def _getClassString(self, cls):
        return cls.__module__ + '.' + cls.__name__
    
