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
from persistent.interfaces import IPersistent
from zope.interface import Interface, Attribute, implements
from zope.app import zapi
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.field import FieldIndex
from zope.app.intid.interfaces import IIntIds
from zope.app.location.interfaces import ILocation
from zope.event import notify
from zope.app.event.objectevent import ObjectEvent
from zope.security.proxy import removeSecurityProxy

from interfaces import IRelationsRegistry, IRelationInvalidatedEvent


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
    
    def query(self, example=None, **kw):
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

    def setupIndexes(self):
        for idx in ('relationship', 'first', 'second', 'third'):
            if idx not in self:
                self[idx] = FieldIndex(idx, IIndexableRelation)

    def register(self, relation):
        if getattr(relation, '__parent__', None) is None:
            # Allow the IntIds utility to get a DB connection:
            relation.__parent__ = self
        self.index_doc(zapi.getUtility(IIntIds).register(relation), relation)
    
    def unregister(self, relation):
        self.unindex_doc(zapi.getUtility(IIntIds).getId(relation))
        notify(RelationInvalidatedEvent(relation))

    def query(self, example=None, **kw):
        for k in kw:
            if k == 'relationship':
                quString = kw[k].getPredicateName()
            else:
                quString = zapi.getUtility(IIntIds).getId(kw[k])
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
        return self.context.getPredicateName()
    relationship = property(getRelationship)

    def __getattr__(self, attr):
        value = getattr(self.context, attr)
        if IPersistent.providedBy(value):
            return zapi.getUtility(IIntIds).getId(value)
        else:
            return value


# convenience function:

def getRelations(first=None, second=None, third=None, relationships=None):
    """ Return a sequence of relations matching the query specified by the
        parameters.

        The relationships parameter expects a sequence of relationships
        (relation classes or predicate objects).
    """
    registry = zapi.getUtility(IRelationsRegistry)
    query = {}
    if first is not None: query['first'] = first
    if second is not None: query['second'] = second
    if third is not None: query['third'] = third
    if not relationships:
        return registry.query(**query)
    else:
        result = set()
        for r in relationships:
            query['relationship'] = r
            result.update(registry.query(**query))
        return result


# events and handlers

class RelationInvalidatedEvent(ObjectEvent):
    implements(IRelationInvalidatedEvent)


def invalidateRelations(context, event):
    """ Handles IObjectRemoved event: unregisters
        all relations the object to be removed is involved in.
    """
    relations = []
    registry = zapi.getUtility(IRelationsRegistry)
    for attr in ('first', 'second', 'third'):
        relations = registry.query(**{attr: context})
        for relation in relations:
            registry.unregister(relation)

def removeRelation(context, event):
    """ Handles IRelationInvalidatedEvent by removing the relation
        (that should be already unregistered from the relations registry)
        from its container (if appropriate) and the IntIds utility.
    """
    if ILocation.providedBy(context):
        parent = zapi.getParent(context)
        if parent is not None:
            del parent[context]
    intids = zapi.getUtility(IIntIds)
    intids.unregister(context)

def setupIndexes(context, event):
    """ Handles IObjectAdded event for the RelationsRegistry utility
        and creates the indexes needed.
    """
    if isinstance(context, RelationsRegistry):
        context.setupIndexes()

