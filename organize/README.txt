Organizations: Persons, Institutions, Addresses...
==================================================

  ($Id$)

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
  
  >>> john.age

  >>> from datetime import date
  >>> john.birthDate = date(1980, 3, 25)
  >>> john.age
  26

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

