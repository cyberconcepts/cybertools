===========================
Schema and Field Management
===========================

  ($Id$)

  >>> from cybertools.composer.schema import Schema
  >>> from cybertools.composer.schema import Field

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
