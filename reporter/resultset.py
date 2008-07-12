#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Example classes for the cybertools.reporter package. These use the
cybertools.contact package

$Id$
"""

# TODO: move the generic stuff to cybertools.reporter.result

from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import Interface, implements

from cybertools.composer.schema import Schema
from cybertools.composer.schema.instance import Instance
from cybertools.reporter.interfaces import IDataSource
from cybertools.reporter.interfaces import IResultSet, IRow, ICell


class Cell(object):
    # TODO: replace Cell by FieldInstance

    implements(ICell)

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


class Row(Instance):

    implements(IRow)

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


class ContentRow(Instance):
    """ A row adapter for standard content objects.
    """

    implements(IRow)
    adapts(Interface)

    @Lazy
    def fields(self):
        return self.template.fields


class ResultSet(object):

    implements(IResultSet)
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
