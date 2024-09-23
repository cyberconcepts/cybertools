==================================================
Organizations: Persons, Institutions, Addresses...
==================================================

  ($Id$)

  >>> from zope import component


Persons and Addresses
=====================

Let's start with a Person:

  >>> from cybertools.organize.party import Person
  >>> john = Person('Smith')
  >>> john.lastName
  'Smith'
  >>> john.firstName
  ''
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

  >>> john.firstName = 'John'
  >>> john.firstName
  'John'

Addresses
---------

Let's create an address and assign it to a person:

  >>> from cybertools.organize.party import Address
  >>> addr = Address('New York', 'Broadway 1')
  >>> john.addresses['standard'] = addr
  >>> john.addresses['standard'].street
  'Broadway 1'


Tasks
=====

  >>> from cybertools.organize.task import Task


Service and Form Management
===========================

See servicemanager.txt and formmanager.txt.

