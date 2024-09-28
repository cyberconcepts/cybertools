===========================
Schema and Field Management
===========================

  >>> from cybertools.composer.schema import Schema
  >>> from cybertools.composer.schema import Field


Working with predefined schemas
===============================

We start with setting up a schema with fields.

  >>> serviceSchema = Schema(
  ...     Field('title', renderFactory=None),
  ...     Field('description'),
  ...     Field('start'),
  ...     Field('end'),
  ...     Field('capacity'),
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
  ('Service', '', '30')

Field types
-----------

  >>> from cybertools.composer.schema.interfaces import fieldTypes
  >>> sorted(t.token for t in fieldTypes)
  ['checkbox', 'checkboxes', 'date', 'decimal', 'display', 'dropdown', 
   'email', 'explanation', 'fileupload', 'heading', 'html', 'list', 'number', 
   'password', 'radiobuttons', 'spacer', 'textarea', 'textline']

  >>> from zope.schema.vocabulary import SimpleVocabulary
  >>> textFieldTypes = SimpleVocabulary([t for t in fieldTypes if t.token in
  ...                                       ('textline', 'textarea',)])
  >>> sorted(t.token for t in textFieldTypes)
  ['textarea', 'textline']

Dynamic default values
----------------------

  >>> idField = Field('id', default='user/title|string:???', defaultValueType='tales')
  >>> idField.getDefaultValue()
  '???'


Creating a schema from an interface
===================================

  >>> from zope.interface import Interface, implementer
  >>> import zope.schema
  >>> from cybertools.composer.schema.factory import SchemaFactory
  >>> component.provideAdapter(SchemaFactory)

  >>> class IPerson(Interface):
  ...    firstName = zope.schema.TextLine(title='First name')
  ...    lastName = zope.schema.TextLine(title='Last name')
  ...    age = zope.schema.Int(title='Age')

  >>> class Person(object):
  ...     def __init__(self, firstName='', lastName='', age=None):
  ...         self.firstName, self.lastName, self.age = firstName, lastName, age
  >>> Person = implementer(IPerson)(Person)

  >>> from cybertools.composer.schema.interfaces import ISchemaFactory
  >>> factory = ISchemaFactory(Person())

  >>> schema = factory(IPerson)
  >>> for f in schema.fields:
  ...     print(f.name, f.title, f.fieldType)
  firstName First name textline
  lastName Last name textline
  age Age number

Using a more specialized schema factory
---------------------------------------

  >>> class PersonSchemaFactory(SchemaFactory):
  ...     def __call__(self, interface, **kw):
  ...         schema = super(PersonSchemaFactory, self).__call__(interface)
  ...         if 'firstName' in schema.fields.keys():
  ...             del schema.fields['firstName']  # don't show first name
  ...         return schema
  >>> component.provideAdapter(PersonSchemaFactory, (IPerson,))

  >>> factory = ISchemaFactory(Person())
  >>> schema = factory(IPerson)
  >>> for f in schema.fields:
  ...     print(f.name, f.title, f.fieldType)
  lastName Last name textline
  age Age number


Access and update a context object using a schema-based form
============================================================

  >>> from zope.publisher.browser import TestRequest
  >>> from cybertools.composer.schema.browser.form import Form

We first have to provide adapters for special field types ('number' in
this case) and an instance adapter that manages the access to the
context object.

  >>> from cybertools.composer.schema.field import NumberFieldInstance
  >>> component.provideAdapter(NumberFieldInstance, name='number')

  >>> from cybertools.composer.schema.instance import Instance
  >>> component.provideAdapter(Instance, adapts=(IPerson,))

  >>> person = Person('John', 'Miller', 33)

Note that the first name is not shown as we excluded it via the schema
factory above. The age field is a number, but is shown here as a
string as the instance is accessed using 'edit' mode, i.e. provide
data suitable for showing on an HTML form.

  >>> form = Form(person, TestRequest())
  >>> form.interface = IPerson
  >>> form.data
  {'lastName': 'Miller', 'age': '33'}

For editing we have to provide another instance adapter.

  >>> from cybertools.composer.schema.instance import Editor
  >>> component.provideAdapter(Editor, name='editor')

  >>> input = dict(lastName='Miller', age='40', action='update')
  >>> request = TestRequest(form=input)
  >>> form = Form(person, request)
  >>> form.interface = IPerson
  >>> form.nextUrl = 'dummy_url'  # avoid hassle with IAbsoluteURL view...

  >>> form.update()
  False

  >>> person.age
  40

Create a new object using a schema-based form
---------------------------------------------

  >>> from cybertools.composer.schema.browser.form import CreateForm
  >>> container = dict()

  >>> input = dict(lastName='Smith', age='28', action='update')
  >>> form = CreateForm(container, TestRequest(form=input))
  >>> form.interface = IPerson
  >>> form.factory = Person

  >>> form.nextUrl = 'dummy_url'  # avoid hassle with IAbsoluteURL view...
  >>> form.getName = lambda x: x.lastName.lower()

  >>> form.data
  {'lastName': 'Smith', 'age': '28'}

  >>> form.update()
  False

  >>> p2 = container['smith']
  >>> p2.lastName, p2.age
  ('Smith', 28)

Macros / renderers
------------------

  >>> fieldRenderers = form.fieldRenderers
  >>> sorted(fieldRenderers.keys())
  ['field', 'field_spacer', 'fields', 'form', 'input_checkbox',
   'input_date', 'input_dropdown', 'input_fileupload', 'input_html',
   'input_list', 'input_password', 'input_textarea', 'input_textline']


Special Field Types
===================

Grids, Records, Key Tables
--------------------------

  >>> from cybertools.composer.schema.grid.field import KeyTableFieldInstance

  >>> ktfield = Field('data')
  >>> ktfield.column_types = [zope.schema.Text(__name__='key', title='Key',),
  ...                         zope.schema.Text(__name__='value', title='Value')]

  >>> ktfi = KeyTableFieldInstance(ktfield)
  >>> ktfi.unmarshall([dict(key='0001', value='First row')])
  {'0001': ['First row']}

  >>> ktfi.marshall({'0001': ['First row']})
  [{'key': '0001', 'value': 'First row'}]

Now with some real stuff, using a field instance that takes the column types
from the context object of the edit form.

  >>> from cybertools.composer.schema.grid.interfaces import KeyTable
  >>> from cybertools.composer.schema.grid.field import \
  ...                               ContextBasedKeyTableFieldInstance
  >>> component.provideAdapter(ContextBasedKeyTableFieldInstance, name='keytable')

  >>> class IDataTable(Interface):
  ...     title = zope.schema.TextLine(title='Title', required=False)
  ...     columnNames = zope.schema.List(title='Column Names', required=False)
  ...     data = KeyTable(title='Data', required=False)
  >>> IDataTable['columnNames'].nostore = True

  >>> class DataTable(object):
  ...     def __init__(self, title, columnNames):
  ...         self.title = title
  ...         self.columnNames = columnNames
  >>> DataTable = implementer(IDataTable)(DataTable)

  >>> dt = DataTable('Account Types', ['identifier', 'label', 'info'])

  >>> input = dict(title='Account Types',
  ...              columnNames=['identifier', 'label', 'info'],
  ...              data=[dict(identifier='0001', label='Standard', info='')],
  ...              action='update')
  >>> form = Form(dt, TestRequest(form=input))
  >>> form.interface = IDataTable
  >>> form.nextUrl = 'dummy_url'
  >>> form.update()
  False

  >>> dt.data
  {'0001': ['Standard', '']}
