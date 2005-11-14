Quickstart Instructions
=======================

  ($Id$)

In the ++etc++/default folder of your Zope 3 site create a Unique Id Utility
and a Relations Registry.

In your application

- define a subclass of DyadicRelation (``MyRelation``)

- create instances of this class that relate objects via
  ``MyRelation(object1, object2)``.

- register these relation objects by getting a utility providing
  ``IRelationsRegistry`` and call the ``register(relation)`` on this utility.
  
You are now ready to retrieve relations by using the relations registry's
``query()`` method as described below.

You may also like to read the file concepts.txt that gives you some more basic
ideas about the relation package.


A Basic API for Relation Management
===================================

In object-oriented programming you usually don't care explicitly about
relations: you just assign an object to an attribute of another object
and you have created a relation beween these two objects.

An example: Let's have two classes, Person and City, and we want to store the
fact that a person lives in a certain city. So if ``clark`` is an instance
of Person and ``washington`` an instance of City we can just say:
``clark.city = washington``.

This works fine (even when you are dealing with persistent objects in Zope)
and is the standard way of establishing a relation in an object-oriented
programming language.

But there are scenarios where this is not sufficient and you have to
care explicitly about relations.

One would be the requirement to get all inhabitants of Washington: You could
of course do this by collecting all persons and check which ones have
set it's ``city`` attribute to ``washington``. This approach poses (at least)
two problems:

- how can I find all instances of the Person class?

- depending on the numbers of persons in my system checking all might take a
  tremendous long time.

You can easiliy resolve these problems by providing a corresponding attribute
on the City class, something like ``washington.inhabitants = [clark]`` and add
a person to this list every time you assign ``washington`` to a person's
``city`` attribute.

Of course there are other things to consider, e.g. how to handle deletions
of objects.

But for this simple kind of relationships just connecting two objects you
could in fact solve all this problems without the need for a special
relation management framework. Nevertheless, as this is a common pattern,
it would be helpful to have an ageed-upon standard how to handle such
cases; this might deal with the automatic housekeeping of redundant
assignments as well as with the deletion problem.

Such a standard - and a corresponding relation management framework - is
getting really important when we deal with more complex use cases - involving
e.g. triadic relations (connecting three objects) like in
"kirk is the child of audrey and clark" or if we want the relation to carry
additional information, e.g. like in
"clark lived in washington from 1999 to 2003".


Relation Management at Work: create - register - query
======================================================

    >>> from zope.app.testing.placelesssetup import setUp
    >>> setUp()

Let's start with two classes and a few objects that we will connect using
relations (we derive the classes from Persistent, thus we will be able to
reference these objects via IntIds later; the __parent__ and __name__
attributes are also needed later when we send an IObjectRemovedEvent event):

    >>> from persistent import Persistent
    >>> class Person(Persistent):
    ...     __name__ = __parent__ = None

    >>> class City(Persistent):
    ...     pass

    >>> clark = Person()
    >>> kirk = Person()
    >>> audrey = Person()
    >>> washington = City()
    >>> newyork = City()

The relation we'll use tells us in which city a person lives; this is a dyadic
relation as it connects two objects. We also associate the relationship
with an interface as we will later use this interface for querying relations.


Dyadic Relations
~~~~~~~~~~~~~~~~

    >>> from cybertools.relation import DyadicRelation
    >>> class LivesIn(DyadicRelation):
    ...     pass

We don't directly keep track of relations but use a relations registry for
this. The relations registry is usually a local utility; for testing we use
a simple dummy implementation:

    >>> from cybertools.relation.registry import DummyRelationsRegistry
    >>> relations = DummyRelationsRegistry()

So we are ready to connect a person and a city using the LivesIn relationship:

    >>> relations.register(LivesIn(clark, washington))
    >>> relations.register(LivesIn(audrey, newyork))
    >>> relations.register(LivesIn(kirk, newyork))

We can now query the relations registry to find out where clark lives and
who lives in New York. For this we use the standard attributes of dyadic
relations, first and second:

    >>> clarkRels = relations.query(first=clark)
    >>> len(clarkRels)
    1
    >>> clarkRels[0].second == washington
    True

    >>> nyRels = relations.query(second=newyork)
    >>> len(nyRels)
    2

It is also possible to remove a relation from the relation registry:

    >>> relations.unregister(
    ...     relations.query(first=audrey, second=newyork)[0]
    ... )
    >>> nyRels = relations.query(second=newyork)
    >>> len(nyRels)
    1
    >>> nyRels[0].first == kirk
    True

    
Triadic Relations
~~~~~~~~~~~~~~~~~

We now extend our setting using a triadic relationship - triadic relations
connect three objects. (If you want to connect more than three objects you
may use combinations of triadic and dyadic relations.)

    >>> from cybertools.relation import TriadicRelation
    >>> class ParentsOf(TriadicRelation):
    ...     """ first (father) and second (mother) are the parents of
    ...         third (child)."""

    >>> relations.register(ParentsOf(clark, audrey, kirk))

When we search for relations that contain clark as first we get both:
    
    >>> clarkRels = relations.query(first=clark)
    >>> len(clarkRels)
    2

So we want to look only for ParentsOf relationships - this should give us
all relations for clark's children:

    >>> clarkChildren = relations.query(relationship=ParentsOf,
    ...                                 first=clark)
    >>> len(clarkChildren)
    1
    >>> clarkChildren[0].second == audrey
    True
    >>> clarkChildren[0].third == kirk
    True

    
Setting up and using a RelationsRegistry local utility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We now do the same stuff as above with a real, catalog-based implementation of
the relations registry. We also register the relations registry as a
utility for demonstration purposes (and to be able to use it later when
working with events).

    >>> from cybertools.relation.registry import RelationsRegistry
    >>> from cybertools.relation.interfaces import IRelationsRegistry
    >>> from zope.app.testing import ztapi
    >>> ztapi.provideUtility(IRelationsRegistry, RelationsRegistry())

    >>> from zope.app import zapi
    >>> relations = zapi.getUtility(IRelationsRegistry)

In real life the indexes needed will be set up via subscription to
IObjectCreatedEvent - here we have to do this explicitly:

    >>> relations.setupIndexes()
    
In order to register relations the objects that are referenced have to be
registered with an IntIds (unique ids) utility, so we have to set up such
an utility (using a stub/dummy implementation for testing purposes) and
register the objects with it (in real life this is done automatically
when we add an object to a container):

    >>> from cybertools.relation.tests import IntIdsStub
    >>> from zope.app.intid.interfaces import IIntIds
    >>> ztapi.provideUtility(IIntIds, IntIdsStub())
    >>> intids = zapi.getUtility(IIntIds)
    >>> intids.register(clark)
    0
    >>> intids.register(kirk)
    1
    >>> intids.register(audrey)
    2
    >>> intids.register(washington)
    3
    >>> intids.register(newyork)
    4

We also have to provide an adapter for the Relation objects that provides
the attributes needed for indexing:

    >>> from cybertools.relation.registry import IIndexableRelation
    >>> from cybertools.relation.registry import IndexableRelationAdapter
    >>> from cybertools.relation.interfaces import IRelation
    >>> ztapi.provideAdapter(IRelation, IIndexableRelation,
    ...                      IndexableRelationAdapter)

So we are ready again to register a set of relations with our new relations
registry and query it.

    >>> relations.register(LivesIn(clark, washington))
    >>> relations.register(LivesIn(audrey, newyork))
    >>> relations.register(LivesIn(kirk, newyork))

As we now get back a result set we have to convert the query results to a list
if we want to access relations by array index:
    
    >>> clarkRels = list(relations.query(first=clark))
    >>> len(clarkRels)
    1
    >>> clarkRels[0].second == washington
    True

    >>> nyRels = relations.query(second=newyork)
    >>> len(nyRels)
    2

    >>> relations.unregister(
    ...     list(relations.query(first=audrey, second=newyork))[0]
    ... )
    >>> nyRels = list(relations.query(second=newyork))
    >>> len(nyRels)
    1
    >>> nyRels[0].first == kirk
    True

It should work also for triadic relations:

    >>> relations.register(ParentsOf(clark, audrey, kirk))

    >>> clarkRels = relations.query(first=clark)
    >>> len(clarkRels)
    2

    >>> clarkChildren = list(relations.query(relationship=ParentsOf,
    ...                                      first=clark))
    >>> len(clarkChildren)
    1
    >>> clarkChildren[0].second == audrey
    True
    >>> clarkChildren[0].third == kirk
    True


Handling object removal
~~~~~~~~~~~~~~~~~~~~~~~

Often it is desirable to unregister a relation when one of the objects
involved in it is removed from its container. This can be
done by subscribing to IObjectRemovedEvent. The relation.registry module
provides a simple handler for this event. (In real life all this is
done via configure.zcml - see relation/configure.zcml for an example that
also provides the default behaviour.)

    >>> from zope.app.container.interfaces import IObjectRemovedEvent
    >>> from zope.app.container.contained import ObjectRemovedEvent
    >>> from zope.event import notify
    >>> from zope.interface import Interface
    >>> from cybertools.relation.registry import invalidateRelations
    
    >>> ztapi.subscribe([Interface, IObjectRemovedEvent], None,
    ...                 invalidateRelations)

The invalidateRelations handler will query for all relations the object to be
removed is involved in and then fire for these relations a
IRelationInvalidatedEvent. This then does the real work.

So we also have to subscribe to this event. We use a standard handler that
removes the relation from whereever it is known that is provided in
the registry module. (There might be other handlers that raise an
exception thus preventing the removal of objects that take part in certain
relations.)

    >>> from cybertools.relation.interfaces import IRelation
    >>> from cybertools.relation.interfaces import IRelationInvalidatedEvent
    >>> from cybertools.relation.registry import removeRelation
    
    >>> ztapi.subscribe([IRelation, IRelationInvalidatedEvent], None,
    ...                 removeRelation)

Let's first check if everything is still as before:

    >>> len(relations.query(first=clark))
    2
    
We simulate the removal of kirk by calling notify, so clark hasn't got
a son any longer :-(
    
    >>> notify(ObjectRemovedEvent(kirk))

Thus there should only remain one relation containing clark as first:

    >>> len(relations.query(first=clark))
    1


Named Predicates
~~~~~~~~~~~~~~~~

Up to now we had to create a new class for each relationship we want to use.
This is also the way the standard implementation works.

But often it is desirable to create new relationships on the fly by
providing some string as the name of the relationship. This can be done by
creating a special relation class that uses named predicates.

    >>> class PredicateRelation(DyadicRelation):
    ...     def __init__(self, predicate, first, second):
    ...         self.predicate = predicate
    ...         self.first = first
    ...         self.second = second
    ...     def getPredicateName(self):
    ...         return self.predicate.getPredicateName()

We also need a class for the predicate objects that will be used for
the constructor of the NamedPredicateRelation class:

    >>> from cybertools.relation.interfaces import IPredicate
    >>> from zope.interface import implements
    
    >>> class Predicate(object):
    ...     implements(IPredicate)
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def getPredicateName(self):
    ...         return self.name

We can now create a predicate with the name '_lives in_' (that may replace
our LivesIn relation class from above) and use for registration:

    >>> livesIn = Predicate('_ lives in _')

    >>> relations.register(PredicateRelation(livesIn, clark, washington))
    >>> relations.register(PredicateRelation(livesIn, audrey, newyork))
    >>> relations.register(PredicateRelation(livesIn, kirk, newyork))

The predicate may then be used as the relationship argument when querying
the relations registry.

    >>> len(relations.query(relationship=livesIn, second=washington))
    1
    >>> len(relations.query(relationship=livesIn, second=newyork))
    2
