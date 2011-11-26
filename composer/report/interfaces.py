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

from cybertools.composer.interfaces import ITemplate, IComponent, ICompound
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


class IReportParams(Interface):
    """ Contains the real reporting parameters like query and sort criteria,
        column definitions, etc.
    """

    queryCriteria = Attribute('The criteria to be used for executing the '
                    'query step.')
    sortSpec = Attribute('A sequence of fields/sort directions to be used for '
                    'executing the sorting step.')
    outputSpec = Attribute('A sequence of output fields (column/cell '
                    'specifications) to be used for presenting the result data.')


class IReport(ITemplate, IReportParams):
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
    owner = schema.ASCIILine(
                title=_(u'Owner'),
                description=_(u'The user ID of the owner of the report.'),
                required=True,)
    public = schema.Bool(
                title=_(u'Public'),
                description=_(u'Check this field to make the report available '
                        u'to others.'),
                required=False,)

    manager = Attribute('The manager of this message object')

    fields = Attribute('An ordered collection of all field definitions '
                    'available for this report type.')
    renderers = Attribute('An ordered collection of renderers available '
                    'for this report type.')

    def getQueryFields():
        """ Return a sequence of fields that may be used for setting up
            the query criteria.
        """

    def getSortFields():
        """ Return a sequence of fields that may be used for setting up
            the sort criteria.
        """

    def getOutputFields():
        """ Return a sequence of fields that may be used for setting up
            the output specification.
        """


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
                title=_(u'Field Name'),
                description=_(u'The internal name of the field.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The visible title or label of the field.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the field.'),
                required=False,)
    fieldType = schema.Choice(
                title=_(u'Field Type'),
                description=_(u'The type of the field.'),
                required=True,
                default='textline',
                vocabulary=fieldTypes,)
    executionSteps = schema.List(
                title=_(u'Execution Steps'),
                description=_(u'The execution steps for which this field may '
                        u'be used.'),
                required=True,
                default=['query', 'sort', 'output'],)


class IBaseReportComponent(IComponent):

    name = schema.ASCII(
                title=_(u'Field Name'),
                description=_(u'The internal name of the field.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The visible title of the field.'),
                required=True,)
    baseName = schema.ASCII(
                title=_(u'Base Field Name'),
                description=_(u'The name of the predefined field specification '
                        u'this field is based on.'),
                required=True,)
    expression = schema.ASCII(
                title=_(u'Expression'),
                description=_(u'Optional: an expression to be applied to '
                        u'the field\'s value before using it in the '
                        u'corresponding execution step.'),
                required=False,)


class IQueryCriteria(Interface):

    def check(obj):
        """ Return True if the object given meets the query conditions
            specified by this criteria object.
        """


class ILeafQueryCriteria(IQueryCriteria, IBaseReportComponent):
    """ A terminal query criteria element.
    """

    operator = schema.Choice(
                title=_(u'Operator'),
                description=_(u'Operator to be used for comparison.'),
                required=True,
                default='in',
                values=('=', '<', '<=', '>', '>=', '!=', 'in'),)
    comparisonValue = schema.Object(
                title=_(u'Comparison Value'),
                description=_(u'The value to be used for comparison.'),
                schema=Interface,
                required=True,)


class ICompoundQueryCriteria(IQueryCriteria, IBaseReportComponent, ICompound):
    """ A query criteria element consisting of leaf query criteria elements.
        The names of the component criteria are given by the ``parts``
        attribute.
    """

    logicalOperator = schema.Choice(
                title=_(u'Operator'),
                description=_(u'Logical operator for connecting the sub-criteria.'),
                required=True,
                default='and',
                values=('and', 'or'),)


class ISortField(IBaseReportComponent):
    """ Specification for a field to be used for sorting.""
    """

    direction = schema.Choice(
                title=_(u'Sort Direction'),
                description=_(u'Sort direction: Ascending or descending.'),
                required=True,
                default='ascending',
                values=('ascending', 'descending'),)


class IOutputField(IBaseReportComponent):
    """ Specification for a field to be used as a table column or cell.""
    """

    label = schema.TextLine(
                title=_(u'Lable'),
                description=_(u'The label to be used when displaying the field.'),
                required=True,)
    format = schema.ASCII(
                title=_(u'Format'),
                description=_(u'A format string for displaying the field.'),
                required=False,)
    instanceName = schema.ASCII(
                title=_(u'Instance Name'),
                description=_(u'The name referencing a field instance class '
                        u'to be used for processing the field\'s value.'),
                required=False,)
