Yet Another Relations Engine...
===============================

Let's start with two classes and a few objects that we will connect using
relations:

    >>> class Person(object):
    ...     pass

    >>> class City(object):
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

Triedic Relations
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

    >>> clarkChildren = relations.query(relationship=ParentsOf, first=clark)
    >>> len(clarkChildren)
    1
    >>> clarkChildren[0].second == audrey
    True
    >>> clarkChildren[0].third == kirk
    True

Setting up and using a RelationsRegistry local utility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

