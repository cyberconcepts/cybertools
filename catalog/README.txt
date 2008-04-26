=========================
Catalog, Indexes, Queries
=========================

  ($Id$)


Set up Working Environment
==========================

We first have to set up an IntIds utility (we use a dummy implementation
for testing purposes here) and a catalog with a few indexes.

  >>> from zope import component
  >>> from cybertools.relation.tests import IntIdsStub
  >>> intid = IntIdsStub()
  >>> component.provideUtility(intid)

  >>> from zope.app.catalog.interfaces import ICatalog
  >>> from zope.app.catalog.catalog import Catalog
  >>> catalog = Catalog()
  >>> component.provideUtility(catalog, ICatalog)

  >>> from zope.interface import Interface, Attribute, implements
  >>> class IContent(Interface):
  ...     f1 = Attribute('f1')
  ...     f2 = Attribute('f2')
  ...     f3 = Attribute('f3')
  ...     t1 = Attribute('t1')
  ...     t2 = Attribute('t2')
  ...     k1 = Attribute('k1')

  >>> from zope.app.catalog.field import FieldIndex
  >>> from zope.app.catalog.text import TextIndex
  >>> from cybertools.catalog.keyword import KeywordIndex
  >>> catalog['f1'] = FieldIndex('f1', IContent)
  >>> catalog['f2'] = FieldIndex('f2', IContent)
  >>> catalog['f3'] = FieldIndex('f3', IContent)
  >>> catalog['t1'] = TextIndex('t1', IContent)
  >>> catalog['t2'] = TextIndex('t2', IContent)
  >>> catalog['k1'] = KeywordIndex('k1', IContent)

In addition we need a class for the content objects that we want
to index and query.

  >>> from zope.app.container.contained import Contained
  >>> class Content(Contained):
  ...     implements(IContent)
  ...     def __init__(self, id, f1='', f2='', f3='', t1='', t2='', k1=[]):
  ...         self.id = id
  ...         self.f1 = f1
  ...         self.f2 = f2
  ...         self.f3 = f3
  ...         self.t1 = t1
  ...         self.t2 = t2
  ...         self.k1 = k1
  ...     def __cmp__(self, other):
  ...         return cmp(self.id, other.id)

The id attribute is just so we can identify objects we find again
easily. By including the __cmp__ method we make sure search results
can be stably sorted.

We are now ready to create a few content objects.

Now let's create some objects so that they'll be cataloged.

  >>> content = [
  ... Content(1, 'a', 'b', 'd'),
  ... Content(2, 'a', 'c'),
  ... Content(3, 'X', 'c'),
  ... Content(4, 'a', 'b', 'e'),
  ... Content(5, 'X', 'b', 'e', k1=('zope', 'plone')),
  ... Content(6, 'Y', 'Z', t1='some interesting text')]

And catalog them now.

  >>> for entry in content:
  ...     catalog.index_doc(intid.register(entry), entry)

Let's provide a simple function for displaying query results.

  >>> def displayQuery(q):
  ...     return [intid.getObject(uid).id for uid in q.apply()]

  >>> def displayQueryWithScores(q):
  ...     return [(intid.getObject(uid).id, score) for uid, score in q.apply().items()]


Field Index Queries
===================

Now for a query where f1 equals a.

  >>> from cybertools.catalog.query import Eq
  >>> f1 = ('', 'f1')
  >>> displayQuery(Eq(f1, 'a'))
  [1, 2, 4]

Not equals (this is more efficient than the generic ~ operator).

  >>> from cybertools.catalog.query import NotEq
  >>> displayQuery(NotEq(f1, 'a'))
  [3, 5, 6]

Testing whether a field is in a set.

  >>> from cybertools.catalog.query import In
  >>> displayQuery(In(f1, ['a', 'X']))
  [1, 2, 3, 4, 5]

Whether documents are in a specified range.

  >>> from cybertools.catalog.query import Between
  >>> displayQuery(Between(f1, 'X', 'Y'))
  [3, 5, 6]

You can leave out one end of the range.

  >>> displayQuery(Between(f1, 'X', None)) # 'X' < 'a'
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(Between(f1, None, 'X'))
  [3, 5]

You can also use greater-equals and less-equals for the same purpose.

  >>> from cybertools.catalog.query import Ge, Le
  >>> displayQuery(Ge(f1, 'X'))
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(Le(f1, 'X'))
  [3, 5]

It's also possible to use not with the ~ operator.

  >>> displayQuery(~Eq(f1, 'a'))
  [3, 5, 6]

Using and (&).

  >>> f2 = ('', 'f2')
  >>> displayQuery(Eq(f1, 'a') & Eq(f2, 'b'))
  [1, 4]

Using or (|).

  >>> displayQuery(Eq(f1, 'a') | Eq(f2, 'b'))
  [1, 2, 4, 5]

These can be chained.

  >>> displayQuery(Eq(f1, 'a') & Eq(f2, 'b') & Between(f1, 'a', 'b'))
  [1, 4]
  >>> displayQuery(Eq(f1, 'a') | Eq(f1, 'X') | Eq(f2, 'b'))
  [1, 2, 3, 4, 5]

And nested.

  >>> displayQuery((Eq(f1, 'a') | Eq(f1, 'X')) & (Eq(f2, 'b') | Eq(f2, 'c')))
  [1, 2, 3, 4, 5]

"and" and "or" can also be spelled differently.

  >>> from cybertools.catalog.query import And, Or
  >>> displayQuery(And(Eq(f1, 'a'), Eq(f2, 'b')))
  [1, 4]
  >>> displayQuery(Or(Eq(f1, 'a'), Eq(f2, 'b')))
  [1, 2, 4, 5]

Combination of In and &
-----------------------

A combination of 'In' and '&'.

  >>> displayQuery(In(f1, ['a', 'X', 'Y', 'Z']))
  [1, 2, 3, 4, 5, 6]
  >>> displayQuery(In(f1, ['Z']))
  []
  >>> displayQuery(In(f1, ['a', 'X', 'Y', 'Z']) & In(f1, ['Z']))
  []


Text Index Queries
==================

  >>> from cybertools.catalog.query import Text
  >>> t1 = ('', 't1')
  >>> displayQuery(Text(t1, 'interesting'))
  [6]


Keyword Index Queries
=====================

  >>> from cybertools.catalog.query import AllOf, AnyOf
  >>> k1 = ('', 'k1')
  >>> displayQuery(AnyOf(k1, 'plone'))
  [5]
  >>> displayQuery(AllOf(k1, ['plone', 'zop']))
  []
  >>> displayQuery(AnyOf(k1, ['plone', 'zop']))
  [5]
  >>> displayQuery(AllOf(k1, ['plone', 'zope']))
  [5]
