Quickstart Instructions
=======================

  ($Id$)

TO DO...

  >>> from zope.app import zapi
  >>> from zope.app.testing import ztapi
  >>> from zope.interface import directlyProvides

A Basic API for Reports and Listings
====================================

Batching
--------

We'll use a fairly simple Iterable:

  >>> it = xrange(14)

  >>> from cybertools.reporter.batch import Batch
  >>> b = Batch(it, size=5, overlap=1, orphan=2)
  >>> b.items
  [0, 1, 2, 3, 4]
  >>> b.getIndexRelative(1)
  1
  >>> b.getIndexAbsolute(-1)
  2

  >>> b = Batch(it, 2, size=5, overlap=1, orphan=2)
  >>> b.items
  [8, 9, 10, 11, 12, 13]

We are now ready to use the corresponding browser view:

  >>> from zope.publisher.browser import TestRequest
  >>> form = dict(b_page=2, b_size=4, b_overlap=1)
  >>> request = TestRequest(form=form)
  >>> from cybertools.reporter.browser.batch import BatchView
  >>> bview = BatchView(None, request)
  >>> bview.setup(it)
  <...BatchView...>
  >>> bview.items()
  [3, 4, 5, 6]
  >>> bview.last
  {'url': 'http://127.0.0.1?b_size=4&b_overlap=1&b_page=5&b_orphan=0',
   'navOnClick': "dojo.io.updateNode(...); return false;",
   'title': 5}

The real reporting stuff
------------------------

  >>> from cybertools.reporter.data import DataSource
  >>> from cybertools.reporter.interfaces import IResultSet

  >>> from cybertools.reporter.example.interfaces import IContactsDataSource
  >>> from cybertools.reporter.example.contact import Contacts

Let's start with the Person class from the example package - we will
then provide a listing of persons...

  >>> from cybertools.organize.party import Person

  >>> from datetime import date
  >>> pdata = ((u'John', u'Smith', '1956-08-01'),
  ...          (u'David', u'Waters', '1972-12-24'),
  ...          (u'Carla', u'Myers', '1981-10-11'))
  >>> persons = DataSource([Person(f, s, date(*[int(d) for d in b.split('-')]))
  ...                         for f, s, b in pdata])
  >>> directlyProvides(persons, IContactsDataSource)

  >>> ztapi.provideAdapter(IContactsDataSource, IResultSet, Contacts)
  >>> rset = IResultSet(persons)

  >>> len(rset)
  3

For the browser presentation we can also use a browser view providing
the result set with extended attributes:

  >>> #rsView = zapi.getMultiAdapter((context, TestRequest()), IBrowserView)

The reporter package also includes facilities for sorting the rows in a
result set and splitting a result into batches.

Sorting
-------


