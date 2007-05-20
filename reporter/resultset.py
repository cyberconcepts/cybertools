#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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

from zope.component import adapts
from zope.interface import implements
from cybertools.reporter.interfaces import IDataSource
from cybertools.reporter.interfaces import IResultSet, IRow, ICell


class Cell(object):

    implements(ICell)

    def __init__(self, field, value, row):
        self.field = field
        self.value = value
        self.row = row

    @property
    def text(self):
        return value

    @property
    def token(self):
        return value

    def sortKey(self):
        return value


class Row(object):

    implements(IRow)

    def __init__(self, context, resultSet):
        self.context = context  # a single object (in this case)
        self.resultSet = resultSet

    @property
    def cells(self):
        schema = self.resultSet.schema
        if schema is None:
            return {}
        return dict([(f.__name__, getattr(self.context, f.__name__))
                        for f in schema.fields])


class ResultSet(object):

    implements(IResultSet)
    adapts(IDataSource)

    def __init__(self, context):
        self.context = context

    _schema = None
    def setSchema(self, schema): self._schema = schema
    def getSchema(self): return self._schema
    schema = property(getSchema, setSchema)

    @property
    def rows(self):
        for o in iter(self.context):
            yield Row(o, self)

