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

from persistent import Persistent
from zope.interface import Interface, Attribute, implements
from zope.app import zapi
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.field import FieldIndex
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

    indexesSetUp = False

    def setupIndexes(self):
        self['relationship'] = FieldIndex('relationship', IIndexableRelation)
        self['first'] = FieldIndex('first', IIndexableRelation)
        self['second'] = FieldIndex('second', IIndexableRelation)
        self['third'] = FieldIndex('third', IIndexableRelation)
        self.indexesSetUp = True

    def register(self, relation):
        if not self.indexesSetUp:
            self.setupIndexes()
        self.index_doc(_getUid(relation), relation)
    
    def unregister(self, relation):
        self.unindex_doc(_getUid(relation))
    
    def query(self, **kw):
        for k in kw:
            if k == 'relationship':
                quString = _getClassString(kw[k])
            else:
                quString = _getUid(kw[k])
            # set min, max
            kw[k] = (quString, quString)
        return self.searchResults(**kw)


    
class IIndexableRelation(Interface):
    """ Provides the attributes needed for indexing relation objects in
        a catalog-based registry.
    """


class IndexableRelationAdapter(object):
    """ Adapter for providing the attributes needed for indexing
        relation objects.
    """

    implements(IIndexableRelation)

    def __init__(self, context):
        self.context = context

    def getRelationship(self):
        return _getRelationship(self.context)
    relationship = property(getRelationship)

    def __getattr__(self, attr):
        value = getattr(self.context, attr)
        if isinstance(value, Persistent):
            return _getUid(value)
        else:
            return value


# helper functions
        
def _getUid(ob):
    return zapi.getUtility(IIntIds).getId(ob)

def _getRelationship(relation):
    return _getClassString(relation.__class__)

def _getClassString(cls):
    return cls.__module__ + '.' + cls.__name__


# event handler

def unregisterRelations(context, event):
    """ Handles IObjectRemoved event: unregisters all relations for the
        object that has been removed.
    """
    relations = []
    registry = zapi.getUtility(IRelationsRegistry)
    for attr in ('first', 'second', 'third'):
        relations = registry.query(**{attr: context})
        for relation in relations:
            registry.unregister(relation)
            # to do: unregister relation also from the IntId utility
            #        (if appropriate).

