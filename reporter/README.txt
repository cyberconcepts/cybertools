Quickstart Instructions
=======================

  ($Id$)

  >>> from zope.app import zapi
  >>> from zope.app.testing import ztapi
  >>> from zope.interface import directlyProvides

A Basic API for Reports and Listings
====================================

  >>> from cybertools.reporter.data import DataSource
  >>> from cybertools.reporter.interfaces import IResultSet

Let's start with the Person class from the example package - we will
then provide a listing of persons...

  >>> from cybertools.reporter.example.contact import Person, Contacts
  >>> from cybertools.reporter.example.interfaces import IContactsDataSource

  >>> import time
  >>> format = '%Y-%m-%d'
  >>> pdata = ((u'John', u'Smith', '1956-08-01'),
  ...          (u'David', u'Waters', '1972-12-24'),
  ...          (u'Carla', u'Myers', '1981-10-11'))
  >>> persons = DataSource([Person(f, s, time.strptime(b, format))
  ...                         for f, s, b in pdata])
  >>> directlyProvides(persons, IContactsDataSource)

  >>> ztapi.provideAdapter(IContactsDataSource, IResultSet, Contacts)
  >>> rset = IResultSet(persons)

For the browser presentation we can also use a browser view providing
the result set with extended attributes:

  >>> #rsView = zapi.getMultiAdapter((context, TestRequest()), IBrowserView)
