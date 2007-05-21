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

from cybertools.composer.schema.schema import Schema
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
        if isinstance(self.value, unicode):
            return self.value
        return unicode(str(self.value))

    @property
    def token(self):
        return self.value

    def sortKey(self):
        return self.value

    @property
    def url(self):
        view = self.row.resultSet.view
        if view is None:
            return ''
        return IAbsoluteURL(self.row, view.request, name=field.__name__)

    @property
    def urlTitle(self):
        return ''


class Row(object):

    implements(IRow)

    def __init__(self, context, resultSet):
        self.context = context
        self.resultSet = resultSet

    @property
    def schema(self):
        return self.resultSet.schema

    @property
    def cells(self):
        for f in self.resultSet.schema.fields:
            yield Cell(f, getattr(self.context, f.name), self)


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

