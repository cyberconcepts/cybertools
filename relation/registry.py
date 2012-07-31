#
#  Copyright (c) 2011 Helmut Merz helmutm@cy55.de
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

from logging import getLogger
from BTrees.IOBTree import IOBTree
from persistent import Persistent
from persistent.interfaces import IPersistent
from zope import component
from zope.component import adapts
from zope.interface import Interface, Attribute, implements
from zope.app.catalog.catalog import Catalog, ResultSet
from zope.app.catalog.field import FieldIndex
from zope.intid.interfaces import IIntIds
from zope.location.interfaces import ILocation
from zope.event import notify
from zope.component.interfaces import ObjectEvent
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName, getParent

from interfaces import IRelationRegistry, IRelationInvalidatedEvent, IRelation


logger = getLogger('cybertools.relation.registry')


class DummyRelationRegistry(object):
    """ Dummy implementation for demonstration and test purposes.
    """

    implements(IRelationRegistry)

    def __init__(self):
        self.relations = []
        self.objects = []

    def register(self, relation):
        if relation not in self.relations:
            self.relations.append(relation)
        if relation not in self.objects:
            self.objects.append(relation)
        for attr in ('first', 'second', 'third',):
            value = getattr(relation, attr, None)
            if value is not None:
                intids = component.queryUtility(IIntIds)
                if intids is not None:
                    intids.register(value)
                elif value not in self.objects:
                    self.objects.append(value)

    def unregister(self, relation):
        if relation in self.relations:
            self.relations.remove(relation)
            notify(RelationInvalidatedEvent(relation))

    def getUniqueIdForObject(self, obj):
        if obj == '*': # wild card
            return '*'
        intids = component.queryUtility(IIntIds)
        if intids is not None:
            return intids.register(obj)
        if obj not in self.objects:
            self.objects.append(obj)
        return self.objects.index(obj)

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
            if r is None:
                continue
            hit = True
            for k in criteria:
                crit = criteria[k]
                if k == 'relationship':
                    critpn = crit.getPredicateName()
                    if critpn.endswith('*'):
                        if not r.getPredicateName().startswith(critpn[:-1]):
                            hit = False; break
                    elif r.getPredicateName() != critpn:
                        hit = False; break
                else:
                    if not hasattr(r, k) or getattr(r, k) != crit:
                        hit = False; break
            if hit:
                result.append(r)
        return result


class RelationRegistry(Catalog):
    """ Local utility for registering (cataloguing) and searching relations.
    """

    implements(IRelationRegistry)

    relations = None

    def __init__(self, *args, **kw):
        super(RelationRegistry, self).__init__(*args, **kw)
        self.relations = IOBTree()

    def setupIndexes(self):
        for idx in ('relationship', 'first', 'second', 'third'):
            if idx not in self:
                self[idx] = FieldIndex(idx, IIndexableRelation)

    def register(self, relation):
        if getattr(relation, '__parent__', None) is None:
            # Allow the IntIds utility to get a DB connection:
            relation.__parent__ = self
        uid = component.getUtility(IIntIds).register(relation)
        self.index_doc(uid, relation)
        if self.relations is not None:
            self.relations[uid] = relation
            #logger.info('added relation with uid %i.' % uid)

    def unregister(self, relation):
        uid = component.getUtility(IIntIds).getId(relation)
        self.unindex_doc(uid)
        if self.relations is not None and uid in self.relations:
            del self.relations[uid]
            #logger.info('removed relation with uid %i.' % uid)
        notify(RelationInvalidatedEvent(relation))

    def cleanupRelations(self):
        logger = getLogger('cybertools.relation.registry.cleanup')
        intids = component.getUtility(IIntIds)
        if self.relations is not None:
            logger.info('%i relations currently stored.' % len(self.relations))
        self.relations = IOBTree()
        result = self.apply(dict(relationship='*'))
        logger.info('%i relations found.' % len(result))
        for idx, uid in enumerate(result):
            relation = intids.getObject(uid)
            self.relations[uid] = relation
        pass

    def getUniqueIdForObject(self, obj):
        if obj == '*': # wild card
            return '*'
        return component.getUtility(IIntIds).queryId(obj)

    def apply(self, criteria):
        for k in criteria:
            # set min, max
            value = criteria[k]
            if k == 'relationship' and value.endswith('*'):
                criteria[k] = (value[:-1], value[:-1] + '\x7f')
            else:
                criteria[k] = (value, value)
        return super(RelationRegistry, self).apply(criteria)

    def query(self, example=None, **kw):
        intids = component.getUtility(IIntIds)
        criteria = {}
        if example is not None:
            for attr in ('first', 'second', 'third',):
                value = getattr(example, attr, None)
                if value is not None:
                    criteria[attr] = intids.getId(value)
            pn = example.getPredicateName()
            if pn is not None:
                criteria['relationship'] = pn
        for k in kw:
            # overwrite example fields with explicit values
            if k == 'relationship':
                criteria[k] = kw[k].getPredicateName()
            else:
                criteria[k] = intids.getId(kw[k])
        results = self.apply(criteria)
        return ResultSet(results, intids)


class IIndexableRelation(Interface):
    """ Provides the attributes needed for indexing relation objects in
        a catalog-based registry.
    """


class IndexableRelationAdapter(object):
    """ Adapter for providing the attributes needed for indexing
        relation objects.
    """

    implements(IIndexableRelation)
    adapts(IRelation)

    def __init__(self, context):
        self.context = context

    def getRelationship(self):
        return self.context.getPredicateName()
    relationship = property(getRelationship)

    def __getattr__(self, attr):
        value = getattr(self.context, attr)
        if IPersistent.providedBy(value):
            return component.getUtility(IIntIds).getId(value)
        else:
            return value


# convenience functions:

def getRelations(first=None, second=None, third=None, relationships=None):
    """ Return a sequence of relations matching the query specified by the
        parameters.

        The relationships parameter expects a sequence of relationships
        (relation classes or predicate objects).
    """
    registry = component.getUtility(IRelationRegistry)
    query = {}
    if first is not None: query['first'] = first
    if second is not None: query['second'] = second
    if third is not None: query['third'] = third
    if not relationships:
        return registry.query(**query)
    else:
        predicates = []
        for r in relationships:
            if hasattr(r, 'predicate'):
                predicates.append(r.predicate)
                r.predicate = None
            else:
                predicates.append(r.getPredicateName())
        result = registry.query(**query)
        if predicates:
            return [r for r in result 
                        if r.ident in predicates or r.fallback in predicates]
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
                '%s, relationship: %s' % (getName(obj),
                                        relationship.getPredicateName()))
    return list(rels)[0]

def setRelationSingle(relation, forSecond=True):
    """ Register the relation given, unregistering already existing
        relations for first and relationship. After this operation there
        will be only one relation for first with the relationship given.
    """
    first = relation.first
    second = relation.second
    registry = component.getUtility(IRelationRegistry)
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
    registries = component.getAllUtilitiesRegisteredFor(IRelationRegistry)
    for registry in registries:
        for attr in ('first', 'second', 'third'):
            try:
                relations = registry.query(**{attr: context})
                for relation in relations:
                    registry.unregister(relation)
            except KeyError:
                pass

def removeRelation(context, event):
    """ Handles IRelationInvalidatedEvent by removing the relation
        (that should be already unregistered from the relation registry)
        from its container (if appropriate) and the IntIds utility.
    """
    if ILocation.providedBy(context):
        parent = getParent(context)
        if parent is not None:
            del parent[context]
    intids = component.getUtility(IIntIds)
    intids.unregister(context)

def setupIndexes(context, event):
    """ Handles IObjectAdded event for the RelationRegistry utility
        and creates the indexes needed.
    """
    if isinstance(context, RelationRegistry):
        context.setupIndexes()

