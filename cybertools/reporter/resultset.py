# cybertools.reporter.resultset

""" Result set and related classes for reporting.

Now obsolete (but still used in some projects),
use cybertools.composer.report.result instead.
"""

# TODO: move the generic stuff to cybertools.reporter.result

from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import Interface, implementer

from cybertools.composer.schema import Schema
from cybertools.composer.schema.instance import Instance
from cybertools.reporter.interfaces import IDataSource
from cybertools.reporter.interfaces import IResultSet, IRow, ICell


@implementer(ICell)
class Cell(object):
    # TODO: replace Cell by FieldInstance

    def __init__(self, field, value, row):
        self.field = field
        self.value = value
        self.row = row

    @property
    def text(self):
        value = self.value
        if value:
            if isinstance(value, unicode):
                return value
            return unicode(str(value))
        return u''

    @property
    def token(self):
        return self.value

    def sortKey(self):
        return self.value

    url = urlTitle = u''


@implementer(IRow)
class Row(Instance):

    def __init__(self, context, resultSet):
        self.context = context
        self.resultSet = resultSet

    @Lazy
    def schema(self):
        return self.resultSet.schema

    @Lazy
    def fields(self):
        return self.schema.fields

    @property
    def cells(self):
        for f in self.schema.fields:
            rf = f.renderFactory or Cell
            yield rf(f, getattr(self.context, f.name), self)


@implementer(IRow)
class ContentRow(Instance):
    """ A row adapter for standard content objects.
    """

    adapts(Interface)

    @Lazy
    def fields(self):
        return self.template.fields


@implementer(IResultSet)
class ResultSet(object):

    adapts(IDataSource)

    view = None

    def __init__(self, context):
        self.context = context
        self.schema = Schema()

    @property
    def rows(self):
        for o in iter(self.context):
            yield Row(o, self)

    def getRows(self):
        for o in iter(self.context):
            row = IRow(o)
            row.resultSet = self
            row.template = self.schema
            yield row
