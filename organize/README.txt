==================================================
Organizations: Persons, Institutions, Addresses...
==================================================

  ($Id$)

  >>> from zope import component


Persons and Addresses
=====================

Let's start with a Person:

  >>> from cybertools.organize.party import Person
  >>> john = Person(u'Smith')
  >>> john.lastName
  u'Smith'
  >>> john.firstName
  u''
  >>> john.birthDate is None
  True
  >>> john.addresses
  {}

A Person object knows the age of the person:

  >>> john.age is None
  True
  >>> from datetime import date
  >>> john.birthDate = date(1980, 3, 25)
  >>> now = date(2006, 5, 12)
  >>> john.ageAt(now)
  26
  >>> john.age >= 26
  True

  >>> john.firstName = u'John'
  >>> john.firstName
  u'John'

Addresses
---------

Let's create an address and assign it to a person:

  >>> from cybertools.organize.party import Address
  >>> addr = Address(u'New York', u'Broadway 1')
  >>> john.addresses['standard'] = addr
  >>> john.addresses['standard'].street
  u'Broadway 1'


Tasks
=====

  >>> from cybertools.organize.task import Task


Service Management
==================

  >>> from cybertools.organize.service import Service

(See cyberapps.tumsm for comprehensive description and tests.)


Work
====

Work items are stored in a tracking storage; in order to conveniently access
the work items we have to provide an adapter to the tracking storage.

  >>> from cybertools.tracking.btree import TrackingStorage
  >>> from cybertools.organize.interfaces import IWorkItems
  >>> from cybertools.organize.work import WorkItemTrack, WorkItems
  >>> component.provideAdapter(WorkItems)

The individual work item (a track) is carrying a state attribute that is
governed by a special states definition. We have to register this states
definition as a utility.

  >>> from cybertools.organize.work import workItemStates
  >>> component.provideUtility(workItemStates(), name='organize.workItemStates')

We are now ready to set up the tracking storage.

  >>> tracks = TrackingStorage(trackFactory=WorkItemTrack)
  >>> workItems = component.getAdapter(tracks, IWorkItems)

The work management only deals with the IDs or names of tasks and persons,
so we do not have to set up real objects.

  >>> workItems.add('001', 'john')
  <WorkItem ['001', 1, 'john', '2008-12-22 12:07', 'created']: {}>
