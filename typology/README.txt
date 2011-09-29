A Basic API for Dynamic Typing
==============================

  ($Id$)

The typology package offers a basic standard API for associating
arbitrary objects with types that may then be used for controlling
execution of code, helping with search interfaces or editing of
object data.

  >>> from zope import component
  >>> from zope.app.testing import ztapi

  >>> from cybertools.typology.interfaces import IType, ITypeManager

Let's start with the Person class from the cybertools.organize package -
we will then apply dynamic typing to Person objects:

  >>> from cybertools.organize.interfaces import IPerson
  >>> from cybertools.organize.party import Person

  >>> from datetime import date
  >>> pdata = ((u'John', u'Smith', '1956-08-01'),
  ...          (u'David', u'Waters', '1972-12-24'),
  ...          (u'Carla', u'Myers', '1999-10-11'))
  >>> persons = [Person(f, s, date(*[int(d) for d in b.split('-')]))
  ...                         for f, s, b in pdata]

Now we want to express that any person younger than 18 years is a
child, and from 18 years on a person is an adult. (Note that this test
will only work until November 2017 ;-))

The example package gives us a class (AgeGroup) for this type
that we use as an adapter to IPerson. The type itself we specify as a
subclass (IAgeGroup) of IType; thus we can associate different types
to one object by providing adapters to different type interfaces.

In addition, the AgeGroup adapter makes use of an AgeGroupManager,
a global utility that does the real work.

  >>> from cybertools.typology.example.person import IAgeGroup, AgeGroup
  >>> ztapi.provideAdapter(IPerson, IAgeGroup, AgeGroup)
  >>> from cybertools.typology.example.person import IAgeGroupManager
  >>> from cybertools.typology.example.person import AgeGroupManager
  >>> ztapi.provideUtility(IAgeGroupManager, AgeGroupManager())

  >>> john_type = IAgeGroup(persons[0])
  >>> david_type = IAgeGroup(persons[1])
  >>> carla_type = IAgeGroup(persons[2])

We can now look what the type is telling us about the persons:

  >>> john_type.title
  u'Adult'
  >>> john_type.token
  'organize.person.agegroup.adult'
  >>> david_type.token
  'organize.person.agegroup.adult'
  >>> carla_type.token
  'organize.person.agegroup.child'

  >>> carla_type.tokenForSearch
  'organize.person.agegroup.child'
  >>> carla_type.qualifiers is None
  True
  >>> carla_type.typeInterface is None
  True
  >>> carla_type.factory is None
  True
  >>> carla_type.defaultContainer is None
  True
  >>> carla_type.typeProvider is None
  True

In this case (and probably a lot of others) types are considered equal
if they have the same token:

  >>> john_type == david_type
  True
  >>> john_type == carla_type
  False

If we want to use this type information on a search form for retrieving
only persons of a certain age group we need a list of available types
(in fact that is an iterable source and, based on it, a vocabulary).

This is where type managers come in. A type manager is a utility or
another (possibly persistent) object knowing about the available types.

  >>> typeManager = component.getUtility(IAgeGroupManager)
  >>> types = typeManager.types
  >>> [t.title for t in types]
  [u'Child', u'Adult']
  >>> types[0] == carla_type
  True
  >>> types[1] == john_type == david_type
  True
  
  >>> t = typeManager.getType(carla_type.token)
  >>> t.title
  u'Child'
