===========================
Schema and Field Management
===========================

  ($Id$)

  >>> from cybertools.composer.schema import Schema
  >>> from cybertools.composer.schema import Field


Working with predefined schemas
===============================

We start with setting up a schema with fields.

  >>> serviceSchema = Schema(
  ...     Field(u'title', renderFactory=None),
  ...     Field(u'description'),
  ...     Field(u'start'),
  ...     Field(u'end'),
  ...     Field(u'capacity'),
  ... )

For using a schema we need some class that we can use for creating
objects.

  >>> class Service(object):
  ...     pass

The schema will be connected with an object via an instance adapter.
In addition, we need a field instance adapter that cares for  the
correct conversion of input data to context attributes.

  >>> from cybertools.composer.schema.instance import Editor
  >>> from cybertools.composer.schema.field import FieldInstance
  >>> from zope import component
  >>> component.provideAdapter(Editor, (Service,), name="service.edit")
  >>> component.provideAdapter(FieldInstance)

  >>> srv = Service()
  >>> inst = component.getAdapter(srv, name='service.edit')
  >>> inst.template = serviceSchema
  >>> inst.applyTemplate(data=dict(title='Service', capacity='30'))
  <...FormState object ...>

  >>> srv.title, srv.description, srv.capacity
  (u'Service', u'', u'30')


Creating a schema from an interface
===================================

  >>> from zope.interface import Interface, implements
  >>> import zope.schema
  >>> from cybertools.composer.schema.factory import SchemaFactory
  >>> component.provideAdapter(SchemaFactory)

  >>> class IPerson(Interface):
  ...    firstName = zope.schema.TextLine(title=u'First name')
  ...    lastName = zope.schema.TextLine(title=u'Last name')
  ...    age = zope.schema.Int(title=u'Age')

  >>> class Person(object):
  ...     implements(IPerson)

  >>> from cybertools.composer.schema.interfaces import ISchemaFactory
  >>> factory = ISchemaFactory(Person())

  >>> schema = factory(IPerson)
  >>> for f in schema.fields:
  ...     print f.name, f.title, f.fieldType
  firstName First name textline
  lastName Last name textline
  age Age number

Using a more specialized schema factory
---------------------------------------

  >>> class PersonSchemaFactory(SchemaFactory):
  ...     def __call__(self, manager=None):
  ...         schema = super(PersonSchemaFactory, self).__call__(manager)
  ...         del schema.fields['firstName']  # don't show first name
  ...         return schema
  >>> component.provideAdapter(PersonSchemaFactory, (IPerson,))

  >>> factory = ISchemaFactory(Person())
  >>> schema = factory(IPerson)
  >>> for f in schema.fields:
  ...     print f.name, f.title, f.fieldType
  lastName Last name textline
  age Age number

