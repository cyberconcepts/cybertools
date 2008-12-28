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

  >>> wi01 = workItems.add('001', 'john')
  >>> wi01
  <WorkItem ['001', 1, 'john', '...', 'new']:
   {'created': ..., 'creator': 'john'}>

Properties that have not been set explicitly have a default of None; properties
not specified in the IWorkItem interface will lead to an AttributeError.

  >>> wi01.description is None
  True
  >>> wi01.something
  Traceback (most recent call last):
  ...
  AttributeError: something

Certain (not all) properties may be set after creation.

  >>> wi01.setInitData(planStart=1229955772, planDuration=600, party='annie')
  >>> wi01
  <WorkItem ['001', 1, 'annie', '2008-12-22 14:22', 'new']:
   {'created': ..., 'planEnd': 1229956372, 'planDuration': 600,
    'planStart': 1229955772, 'creator': 'john', 'planEffort': 600}>

It's possible to change a value after it has been set as long as the work
item is in state 'new'.

  >>> wi01.setInitData(planEffort=700)
  >>> wi01.planEffort
  700

  >>> wi01.setInitData(party='jim')
  >>> wi01.userName
  'jim'

Change work item state
----------------------

Now Jim accepts the work item, i.e. he wants to work on it. Now the party
that the work item is assigned to may not be changed any more.

  >>> wi01.assign()
  >>> wi01.state
  'assigned'
  >>> wi01.setInitData(party='annie')
  Traceback (most recent call last):
  ...
  ValueError: Attribute 'party' already set to 'jim'.

Jim now really starts to work. The start time is usually set automatically
but may also be specified explicitly.

  >>> wi01.startWork(start=1229958000)
  >>> wi01
  <WorkItem ['001', 1, 'jim', '2008-12-22 15:00', 'running']:
   {'created': ..., 'planEnd': 1229956372, 'start': 1229958000,
    'assigned': ..., 'planDuration': 600, 'planStart': 1229955772,
    'creator': 'john', 'planEffort': 700}>

Stopping work
-------------

After five minutes of work Jim decides to stop working; but he will
continue work later, so he executes a ``continue`` transition that will
set up a copy of the work item.

He also specifies a new plan start and duration for the new work item.
Plan end and plan effort are given explicitly as None values so that they
won't be taken from the old work item but recalculated.

Note that the work item has already been set to assigned as Jim has
committed himself to continue working on it by selecting the ``continue``
transition.

  >>> wi02 = wi01.stopWork('continue', end=1229958300, planStart=1229960000,
  ...                      planDuration=400, planEnd=None, planEffort=None)
  >>> wi02
  <WorkItem ['001', 1, 'jim', '2008-12-22 15:33', 'assigned']:
   {'predecessor': '0000001', 'created': ..., 'planEnd': 1229960400,
    'assigned': ..., 'planDuration': 400, 'planStart': 1229960000,
    'creator': 'jim', 'planEffort': 400}>
