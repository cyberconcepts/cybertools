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

  >>> from cybertools.composer.schema.instance import Editor
  >>> from zope import component
  >>> component.provideAdapter(Editor, (Service,), name="service.edit")

  >>> srv = Service()
  >>> inst = component.getAdapter(srv, name='service.edit')
  >>> inst.template = serviceSchema
  >>> inst.applyTemplate()
  title -
  description -
  start -
  end -
  capacity -
