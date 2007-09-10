#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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

_ = MessageFactory('zope')


class ISchema(ITemplate):
    """ Represents an ordered sequence of fields.
    """

    name = schema.ASCII(
                title=_(u'Schema name'),
                description=_(u'The internal name of the schema; will be used '
                'to identify data fields of instance objects that '
                'are associated with this schema.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the schema'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the item.'),
                required=False,)

    fields = Attribute('The components the schema is built up of. '
                'Should be a sequence of IField objects.')
    manager = Attribute('A manager object that may provide special '
                'features, e.g. a factory for objects to be associated '
                'with this schema.')


class FieldType(SimpleTerm):

    def __init__(self, value, token=None, title=None, **kw):
        super(FieldType, self).__init__(value, token, title)
        self.name = value
        self.fieldMacro = 'field'
        self.inputMacro = 'input_' + self.name
        self.storeData = True
        self.instanceName = ''
        for k, v in kw.items():
            setattr(self, k, v)


fieldTypes = SimpleVocabulary((
    FieldType('textline', 'textline', u'Textline'),
    FieldType('textarea', 'textarea', u'Textarea'),
    FieldType('number', 'number', u'Number', inputMacro='input_textline',
              instanceName='number'),
    #FieldType('date', 'date', u'Date'),
    #FieldType('checkbox', 'checkbox', u'Checkbox'),
    FieldType('dropdown', 'dropdown', u'Drop-down selection'),
    FieldType('spacer', 'spacer', u'Spacer', fieldMacro='field_spacer',
              storeData=False),
))

standardFieldNames = SimpleVocabulary((
    SimpleTerm('', '', 'Not selected'),
    SimpleTerm('lastName', 'lastName', 'Last name'),
    SimpleTerm('firstName', 'firstName', 'First name'),
    SimpleTerm('organization', 'organization', 'Organization'),
    SimpleTerm('email', 'email', 'E-Mail address'),
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
    defaultValue = schema.TextLine(
                title=_(u'Default'),
                description=_(u'Value with which to pre-set the field contents'),
                required=False,)
    required = schema.Bool(
                title=_(u'Required'),
                description=_(u'Must a value been entered into this field?'),
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

    renderFactory = Attribute('A class or another factory providing an '
                        'object used for rendering the data e.g. as a '
                        'cell on a tabular report. See cybertools.reporter. '
                        'May become replaced with a more intelligent kind of '
                        'field instance.')


class IFieldInstance(Interface):
    """ An adapter for checking and converting data values coming
        from or being displayed on an external system (like a browser form).
        It also keeps information on the processing state.
    """

    name = Attribute('Field name.')
    change = Attribute('A tuple ``(oldValue, newValue)`` or None.')
    errors = Attribute('A sequence of error infos.')
    severity = Attribute("An integer giving a state or error "
                    "code, 0 meaning 'OK'.")

    def marshall(value):
        """ Return a string (possibly unicode) representation of the
            value given that may be used for editing.
        """

    def display(value):
        """ Return a string (possibly unicode) representation of the
            value given that may be used for presentation.
        """

    def unmarshall(strValue):
        """ Return the internal (real) value corresponding to the string
            value given.
        """

    def validate(value):
        """ Check if the value given is valid. Return an object implementing
            IFieldState.
        """


class IFormState(Interface):
    """ Represents the state of all fields when editing.
    """

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

