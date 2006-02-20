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

from interfaces import IRelationRegistry, IRelationInvalidatedEvent


class DummyRelationRegistry(object):
    """ Dummy implementation for demonstration and test purposes.
    """

    implements(IRelationRegistry)

    def __init__(self):
        self.relations = []

    def register(self, relation):
        if relation not in self.relations:
            self.relations.append(relation)
    
    def unregister(self, relation):
        if relation in self.relations:
            self.relations.remove(relation)
            notify(RelationInvalidatedEvent(relation))
    
    def query(self, example=None, **kw):
        result = []
        criteria = {}
        if example is not None:
            for attr in ('first', 'second', 'third',):
                value = getattr(example, attr, None)
                if value is not None:
                    criteria[attr] = value
            criteria['relationship'] = example
        criteria.update(kw)
        for r in self.relations:
            hit = True
            for k in criteria:
                if ((k == 'relationship'
                        and r.getPredicateName() != criteria[k].getPredicateName())
                 or (k != 'relationship'
                        and (not hasattr(r, k) or getattr(r, k) != criteria[k]))):
                    hit = False
                    break
            if hit:
                result.append(r)
        return result


class RelationRegistry(Catalog):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    implements(IRelationRegistry)

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
        intIds = zapi.getUtility(IIntIds)
        criteria = {}
        if example is not None:
            for attr in ('first', 'second', 'third',):
                value = getattr(example, attr, None)
                if value is not None:
                    criteria[attr] = intIds.getId(value)
            pn = example.getPredicateName()
            if pn:
                criteria['relationship'] = pn
        for k in kw:
            # overwrite example fields with explicit values
            if k == 'relationship':
                criteria[k] = kw[k].getPredicateName()
            else:
                criteria[k] = intIds.getId(kw[k])
        for k in criteria:
            # set min, max
            criteria[k] = (criteria[k], criteria[k])
        return self.searchResults(**criteria)

#BBB
#RelationsRegistry = RelationRegistry


    
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


# convenience functions:

def getRelations(first=None, second=None, third=None, relationships=None):
    """ Return a sequence of relations matching the query specified by the
        parameters.

        The relationships parameter expects a sequence of relationships
        (relation classes or predicate objects).
    """
    registry = zapi.getUtility(IRelationRegistry)
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

def getRelationSingle(obj=None, relationship=None, forSecond=True):
    """ Returns the one and only relation for first having relationship
        or None if there is none.

        Raise an error if there is more than one hit.
    """
    if forSecond:
        rels = getRelations(second=obj, relationships=[relationship])
    else:
        rels = getRelations(first=obj, relationships=[relationship])
    if len(rels) == 0:
        return None
    if len(rels) > 1:
        raise ValueError('Multiple hits when only one relation expected: '
                '%s, relationship: %s' % (zapi.getName(obj),
                                        relationship.getPredicateName()))
    return list(rels)[0]

def setRelationSingle(relation, forSecond=True):
    """ Register the relation given, unregistering already existing
        relations for first and relationship. After this operation there
        will be only one relation for first with the relationship given.
    """
    first = relation.first
    second = relation.second
    registry = zapi.getUtility(IRelationRegistry)
    if forSecond:
        rels = list(registry.query(second=second, relationship=relation))
    else:
        rels = list(registry.query(first=first, relationship=relation))
    for oldRel in rels:
        registry.unregister(oldRel)
    registry.register(relation)

        
# events and handlers

class RelationInvalidatedEvent(ObjectEvent):
    implements(IRelationInvalidatedEvent)


def invalidateRelations(context, event):
    """ Handles IObjectRemoved event: unregisters
        all relations the object to be removed is involved in.
    """
    # TODO: check marker interface of object:
    # if not IRelatable.providedBy(event.object):
    #     return
    relations = []
    #registry = zapi.queryUtility(IRelationRegistry)
    registries = zapi.getAllUtilitiesRegisteredFor(IRelationRegistry)
    for registry in registries:
        for attr in ('first', 'second', 'third'):
            relations = registry.query(**{attr: context})
            for relation in relations:
                registry.unregister(relation)

def removeRelation(context, event):
    """ Handles IRelationInvalidatedEvent by removing the relation
        (that should be already unregistered from the relation registry)
        from its container (if appropriate) and the IntIds utility.
    """
    if ILocation.providedBy(context):
        parent = zapi.getParent(context)
        if parent is not None:
            del parent[context]
    intids = zapi.getUtility(IIntIds)
    intids.unregister(context)

def setupIndexes(context, event):
    """ Handles IObjectAdded event for the RelationRegistry utility
        and creates the indexes needed.
    """
    if isinstance(context, RelationRegistry):
        context.setupIndexes()

