====================================
A Basic API for Reports and Listings
====================================

Note: The basic reporting stuff (with Report, ReportInstance, Field, and ResultSet
classes) is now in cybertools.composer.report. The stuff defined here is,
however, still used in some (TUM) projects and may also be useful in other
cases.

TO DO...

  >>> from zope import component


Listings
========

  >>> from cybertools.reporter.data import DataSource

Let's start with the Person class from the cybertools.organize package - we will
then provide a listing of persons...

  >>> from cybertools.organize.party import Person

  >>> from datetime import date
  >>> pdata = (('John', 'Smith', '1956-08-01'),
  ...          ('David', 'Waters', '1972-12-24'),
  ...          ('Carla', 'Myers', '1981-10-11'))
  >>> persons = DataSource([Person(f, s, date(*[int(d) for d in b.split('-')]))
  ...                         for f, s, b in pdata])

  >>> from cybertools.reporter.resultset import ResultSet, ContentRow
  >>> from cybertools.reporter.interfaces import IResultSet, IRow
  >>> component.provideAdapter(ResultSet)
  >>> component.provideAdapter(ContentRow, provides=IRow)

  >>> from cybertools.composer.schema.schema import Schema
  >>> from cybertools.composer.schema.field import Field
  >>> from cybertools.composer.schema.field import FieldInstance, DateFieldInstance
  >>> component.provideAdapter(FieldInstance)
  >>> component.provideAdapter(DateFieldInstance, name='date')

  >>> rset = IResultSet(persons)
  >>> rset.schema = Schema(Field('firstName'), Field('lastName'),
  ...                      Field('birthDate', fieldType='date'))

  >>> rows = list(rset.getRows())
  >>> len(rows)
  3

  >>> for r in rows:
  ...     print(r.applyTemplate())
  {'firstName': 'Smith', 'lastName': 'John', 'birthDate': '1956-08-01'}
  {'firstName': 'Waters', 'lastName': 'David', 'birthDate': '1972-12-24'}
  {'firstName': 'Myers', 'lastName': 'Carla', 'birthDate': '1981-10-11'}

For the browser presentation we can also use a browser view providing
the result set with extended attributes:

  >>> #rsView = component.getMultiAdapter((rset, TestRequest()), IBrowserView)


The reporter package also includes facilities for sorting the rows in a
result set and splitting a result into batches.

Sorting
=======


Batching
========

We'll use a fairly simple Iterable:

  >>> it = range(14)

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
  {'title': 5, 'url': 'http://127.0.0.1?b_page=5&b_size=4&b_overlap=1&b_orphan=0',
   'navOnClick': "dojo.io.updateNode(...); return false;"}


