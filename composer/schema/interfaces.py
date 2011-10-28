#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Schemas and Fields.

$Id$
"""

from zope import schema
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cybertools.composer.interfaces import ITemplate, IComponent
from cybertools.composer.interfaces import IInstance as IBaseInstance

_ = MessageFactory('cybertools.composer.schema')


class ISchema(ITemplate):
    """ Represents an ordered sequence of fields.
    """

    name = schema.ASCII(
                title=_(u'Schema name'),
                description=_(u'The internal name of the schema; will be used '
                    u'to identify data fields of instance objects that '
                    u'are associated with this schema.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the schema'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the item.'),
                required=False,)
    labelWidth = schema.TextLine(
                title=_(u'Label column width'),
                description=_(u'The width of the label column; please enter '
                    u'a value like used for CSS style sheets, '
                    u'e.g. "200px" or "20%".'),
                default=u'auto',
                required=False,)

    fields = Attribute('The components the schema is built up of. '
                'Should be a sequence of IField objects.')
    manager = Attribute('A manager object that may provide special '
                'features, e.g. a factory for objects to be associated '
                'with this schema.')


class ISchemaFactory(Interface):
    """ Provides a schema when called. Typically used for adapters.
    """

    def __call__(interface, **kw):
        """ Return a schema, based on the interface given.
        """


class FieldType(SimpleTerm):

    hidden = False

    def __init__(self, value, token=None, title=None, **kw):
        super(FieldType, self).__init__(value, token, title)
        self.name = value
        self.fieldRenderer = 'field'
        self.inputRenderer = 'input_' + self.name
        self.displayRenderer = 'display_textline'
        self.storeData = True
        self.instanceName = ''
        for k, v in kw.items():
            setattr(self, k, v)


# TODO: register this object as a utility providing IFieldTypes
fieldTypes = SimpleVocabulary((
    FieldType('textline', 'textline', u'Textline'),
    FieldType('password', 'password', u'Password',
              displayRenderer='display_password'),
    FieldType('textarea', 'textarea', u'Textarea'),
    FieldType('html', 'html', u'HTML Text'),
    FieldType('number', 'number', u'Number',
              inputRenderer='input_textline', instanceName='number'),
    FieldType('date', 'date', u'Date', instanceName='date'),
    FieldType('email', 'email', u'E-Mail Address',
              displayRenderer='display_email', inputRenderer='input_textline',
              instanceName='email'),
    FieldType('fileupload', 'fileupload', u'File upload',
              instanceName='fileupload'),
    FieldType('checkbox', 'checkbox', u'Checkbox', instanceName='boolean'),
    FieldType('dropdown', 'dropdown', u'Drop-down selection',
              instanceName='dropdown'),
    FieldType('radiobuttons', 'radiobuttons', u'Radiobutton Group'),
    #FieldType('listbox', 'listbox', u'List box (multiple selection)'),
    FieldType('list', 'list', u'List', instanceName='list'),
    FieldType('checkboxes', 'checkboxes', u'Checkbox Group',
              instanceName='checkboxes'),
    FieldType('calculated', 'display', u'Calculated Value',
              instanceName='calculated'),
    FieldType('heading', 'heading', u'Fieldgroup Heading',
              fieldRenderer='field_heading', storeData=False),
    FieldType('spacer', 'spacer', u'Spacer',
              fieldRenderer='field_spacer', storeData=False),
    FieldType('explanation', 'explanation', u'Explanation',
              fieldRenderer='field_explanation', storeData=False),
))

# TODO: move this to organize.service... (???)
standardFieldNames = SimpleVocabulary((
    SimpleTerm('', '', 'Not selected'),
    SimpleTerm('lastName', 'lastName', 'Last name'),
    SimpleTerm('firstName', 'firstName', 'First name'),
    SimpleTerm('organization', 'organization', 'Organization'),
    SimpleTerm('email', 'email', 'E-Mail address'),
    SimpleTerm('number', 'number', 'Number of participants'),
    # TODO: on organize.service: extend this list, e.g. with 'totalCost'
))

defaultValueTypes = SimpleVocabulary((
    SimpleTerm('static', 'static', 'Static data'),
    SimpleTerm('tales', 'tales', 'TAL expression'),
))


class IField(IComponent):
    """ May be used for data entry or display.
    """

    name = schema.ASCII(
                title=_(u'Field name'),
                description=_(u'The internal name of the field'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the field'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the field'),
                required=False,)
    fieldType = schema.Choice(
                title=_(u'Field type'),
                description=_(u'The type of the field'),
                required=True,
                default='textline',
                vocabulary=fieldTypes,)
    standardFieldName = schema.Choice(
                title=_(u'Standard field name'),
                description=_(u'Provide the values entered in this field '
                        'as one of the standard informations.'),
                required=False,
                default='',
                vocabulary=standardFieldNames,)
    defaultValueExpr = schema.TextLine(
                title=_(u'Default'),
                description=_(u'Value with which to pre-set the field contents. '
                        'Use this also for populating a calculated field.'),
                required=False,)
    defaultValueType = schema.Choice(
                title=_(u'Default type'),
                description=_(u'The type of the default, i.e. a static value '
                        u'or an expression that is used to calculate the value.'),
                required=False,
                default='static',
                vocabulary=defaultValueTypes)
    required = schema.Bool(
                title=_(u'Required'),
                description=_(u'Must a value be entered into this field?'),
                required=False,)
    width = schema.Int(
                title=_(u'Width'),
                description=_(u'The horizontal size of the field in pixels'),
                default=300,
                required=False,)
    height = schema.Int(
                title=_(u'Height'),
                description=_(u'The vertical size of the field in lines '
                        '(only for type textarea)'),
                default=3,
                required=False,)
    vocabulary = schema.Text(
                title=_(u'Vocabulary'),
                description=_(u'Values that may be selected as values for '
                        'this field; enter one value per line '
                        '(only for dropdown and other selection fields)'),
                required=False,)

    fieldRenderer = Attribute('Name of a renderer (i.e. a ZPT macro or '
                        'an adapter) that is responsible for rendering '
                        '(presenting) the field as a whole.')
    displayRenderer = Attribute('Name of a renderer (i.e. a ZPT macro or '
                        'an adapter) that is responsible for displaying '
                        'field data.')
    inputRenderer = Attribute('Name of a renderer (i.e. a ZPT macro or '
                        'an adapter) that is responsible for rendering '
                        '(presenting) the part of the field that allows '
                        'data input.')
    storeData = Attribute('Boolean value, true when this field provides '
                        'data that may be stored in a context object, '
                        'false for dummy fields like spacers.')

    renderFactory = Attribute('A class or another factory providing an '
                        'object used for rendering the data e.g. as a '
                        'cell on a tabular report. See cybertools.reporter. '
                        'May become replaced with a more intelligent kind of '
                        'field instance.')


undefined = object()    # A marker for a field instance value not set.

class IFieldInstance(Interface):
    """ An adapter for checking and converting data values coming
        from or being displayed on an external system (like a browser form).
        It also keeps information on the processing state.
    """

    name = Attribute('Field name.')
    change = Attribute('A tuple ``(oldValue, newValue)`` or None.')
    errors = Attribute('A sequence of error infos.')
    severity = Attribute('An integer giving a state or error '
                    'code, 0 meaning OK.')
    clientInstance = Attribute('An optional adapter to a client object that '
                    'provides or receives data processed by this field instance.')
    value = Attribute ('May contain the current value of the field '
                    'for later reuse. Default is ``undefined``. '
                    'If the ``change`` attribute is set ``value`` should '
                    'be equal to ``change[1]``.')

    def getRawValue(data, key, default=None):
        """ Extract a raw value for the field from the data given
            using the key; if no corresponding value is found return
            the default. The value returned may then be turned
            byt self.unmarshall() to the real (internal) value.
        """

    def marshall(value):
        """ Return a string (possibly unicode) representation of the
            value given that may be used for editing. In case of complex
            or structured fields (list, mapping, object fields) the return
            value may also be a structured object (typically a list or
            mapping) built up form string (unicode) values.
        """

    def display(value):
        """ Return a string- (possibly unicode-) based representation of the
            value given that may be used for presentation.
        """

    def unmarshall(inputValue):
        """ Return the internal (real) value corresponding to the
            input (external, raw) value given.
        """

    def validate(value, data=None):
        """ Check if the value given is valid. Return an object implementing
            IFieldState.

            Optionally, in addition the full data set may be given to
            allow for checking more than one data element.
        """

    def getRenderer(name):
        """ Return the renderer object (e.g. a ZPT macro) for this field
            with the name given.

            May return None in which case the calling application should
            use a default renderer.
        """


class IFormState(Interface):
    """ Represents the state of all fields when editing.
    """

    fieldInstances = Attribute('A mapping ``{fieldName: fieldInstance, ...}``.')
    changed = Attribute('True if one of the fields has been changed')
    severity = Attribute("An integer giving an overall state or error "
                    "code, typically the maximum of the field instances' "
                    "severities.")


class IInstance(IBaseInstance):
    """ An instance adapter for arbitrary client objects, using a schema.
    """

    fieldInstances = Attribute('A mapping ``{fieldName: fieldInstance, ...}``.')


class IEditor(IInstance):
    """ An instance adapter for a client object that represents the state
        of all fields when editing.
    """
    # TODO: make IFormState + implementations obsolete

    fieldInstances = Attribute('A mapping ``{fieldName: fieldInstance, ...}``.')
    changed = Attribute('True if one of the fields has been changed')
    severity = Attribute("An integer giving an overall state or error "
                    "code, typically the maximum of the field instances' "
                    "severities.")


# clients

class IClient(Interface):
    """ An fairly abstract interface for objects to be used as clients
        for other objects (e.g. services).
    """

    manager = Attribute('The object that cares for this client.')


class IClientFactory(Interface):
    """ Creates client objects.
    """

    def __call__():
        """ Creates and returns a client object.
        """


clientManagerViews = SimpleVocabulary((
    SimpleTerm('', '', u'Default view'),
    SimpleTerm('redirect_registration.html', 'redirect_registration.html',
               u'Redirect to registration')
))

class IClientManager(Interface):
    """ Cares for a client typically providing schemas.
    """

    clients = Attribute('A collection of client objects (e.g. persons) '
                'associated with this client manager.')
    clientSchemas = Attribute('A collection of schema objects '
                'that describe the data fields of the client '
                'objects.')

    def addClient(client):
        """ Add the client object given to the collection of clients.
        """


class IFormManager(IClientManager):
    """ A standalone object that manages client data via one or more
        schema objects.
    """

    senderEmail = schema.TextLine(
                title=_(u'Sender email'),
                description=_(u'Email address that will be used as sender '
                        'address of confirmation and feedback messages.'),
                required=False,)
