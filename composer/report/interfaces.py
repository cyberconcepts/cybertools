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
Report management.

$Id$
"""

from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cybertools.composer.interfaces import ITemplate, IComponent
from cybertools.composer.interfaces import IInstance

_ = MessageFactory('cybertools.composer')


class IReportManager(Interface):
    """ A manager (or container) for reports.
    """

    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the object.'),
                required=True,)

    reports = Attribute('A collection of message objects managed.')

    def addReport(report):
        """ Add a report.
        """

    def getReport(id):
        """ Retrieve a report.
        """


class IReport(ITemplate):
    """ A configurable report.
    """

    identifier = schema.ASCIILine(
                title=_(u'Identifier'),
                description=_(u'The (internal) identifier of the report.'),
                required=True,)
    name = schema.ASCIILine(
                title=_(u'Name'),
                description=_(u'The (visible) name of the report.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the report.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the report.'),
                required=False,)

    manager = Attribute('The manager of this message object')

    fields = Attribute('An ordered collection of all field definitions '
                    'available for this report.')
    renderers = Attribute('An ordered collection of renderers for this report.')


class FieldType(SimpleTerm):

    instanceName = ''

    def __init__(self, value, token=None, title=None, **kw):
        super(FieldType, self).__init__(value, token, title)
        self.name = value
        for k, v in kw.items():
            setattr(self, k, v)

fieldTypes = SimpleVocabulary((
    FieldType('textline', 'textline', u'Textline'),
    FieldType('number', 'number', u'Number', instanceName='number'),
    FieldType('date', 'date', u'Date', instanceName='date'),
))


class IField(IComponent):
    """ Describes a field that may be used in query criteria, for specifying
        columns or cells for display, or for sorting.
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
