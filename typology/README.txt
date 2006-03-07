Quickstart Instructions
=======================

  ($Id$)

  >>> from zope.app import zapi
  >>> from zope.app.testing import ztapi
  >>> from zope.interface import directlyProvides

A Basic API for Dynamic Typing
==============================

  >>> from cybertools.typology.interfaces import IType, ITypeManager

Let's start with the Person class from the cybertools.contact package -
we will then apply dynamic typing to Person objects:

  >>> from cybertools.contact.interfaces import IPerson
  >>> from cybertools.contact import Person

  >>> from datetime import date
  >>> pdata = ((u'John', u'Smith', '1956-08-01'),
  ...          (u'David', u'Waters', '1972-12-24'),
  ...          (u'Carla', u'Myers', '1999-10-11'))
  >>> persons = [Person(f, s, date(*[int(d) for d in b.split('-')]))
  ...                         for f, s, b in pdata]

Now we want to express that any person younger than 18 years is a
child, and from 18 years on a person is an adult. (Note that this test
will only work until November 2017 ;-))

The example package gives us a class for this type that we use as an
adapter to IPerson:

  >>> from cybertools.typology.example.person import BasicAgeGroup
  >>> ztapi.provideAdapter(IPerson, IType, BasicAgeGroup)
  >>> john_type = IType(persons[0])
  >>> david_type = IType(persons[1])
  >>> carla_type = IType(persons[2])

We can now look what the type is telling us about the persons:

  >>> john_type.title
  u'Adult'
  >>> john_type.token
  'contact.person.agetype.adult'
  >>> david_type.token
  'contact.person.agetype.adult'
  >>> carla_type.token
  'contact.person.agetype.child'

Usually types are equal if they have the same token:

  >>> john_type == david_type
  True
  >>> john_type == carla_type
  False
