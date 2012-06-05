#
#  Copyright (c) 2012 Helmut Merz helmutm@cy55.de
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
Report result sets and related classes.
"""

from copy import copy
from zope.cachedescriptors.property import Lazy

from cybertools.composer.interfaces import IInstance
from cybertools.composer.report.base import BaseQueryCriteria


class BaseRow(object):

    def __init__(self, context, parent):
        self.context = context
        self.parent = parent
        self.data = {}
        self.sequenceNumber = 0

    def getRawValue(self, attr):
        return self.data.get(attr)


class Row(BaseRow):

    attributeHandlers = {}

    def getRawValue(self, attr):
        return self.attributeHandlers.get(attr, self.getContextAttr)(self, attr)

    @staticmethod
    def getContextAttr(obj, attr):
        return getattr(obj.context, attr)

    def getGroupFields(self):
        return [self.getRawValue(f.name) for f in
                    self.parent.context.fields if 'group' in f.executionSteps]

    @Lazy
    def displayedColumns(self):
        return self.parent.context.getActiveOutputFields()

    def useRowProperty(self, attr):
        return getattr(self, attr)

    
class GroupHeaderRow(BaseRow):

    def getRawValue(self, attr):
        return self.data.get(attr, u'')

    @Lazy
    def displayedColumns(self):
        fields = self.parent.context.getActiveOutputFields()
        for col in self.headerColumns:
            for idx, f in enumerate(fields):
                if f.name == col.name:
                    fields[idx] = col
        return fields


class ResultSet(object):

    def __init__(self, context, data, rowFactory=Row, headerRowFactory=GroupHeaderRow,
                 sortCriteria=None, queryCriteria=BaseQueryCriteria()):
        
        self.context = context  # the report or report instance
        self.data = data
        self.rowFactory = rowFactory
        self.headerRowFactory = headerRowFactory
        self.sortCriteria = sortCriteria
        self.queryCriteria = queryCriteria
        self.totals = BaseRow(None, self)

    def getHeaderRow(self, row, columns):
        headerRow = self.headerRowFactory(None, self)
        headerRow.headerColumns = []
        for c in columns:
            if c.output:
                headerRow.data[c.output] = c.getRawValue(row)
                headerColumn = copy(c)
                headerColumn.__name__ = c.output
                headerRow.headerColumns.append(headerColumn)
        return headerRow
            
    def getResult(self):
        result = [self.rowFactory(item, self) for item in self.data]
        result = [row for row in result if self.queryCriteria.check(row)]
        if self.sortCriteria:
            result.sort(key=lambda x: [f.getSortValue(x) for f in self.sortCriteria])
        if self.groupColumns:
            res = []
            groupValues = [None for f in self.groupColumns]
            for row in result:
                for idx, f in enumerate(self.groupColumns):
                    value = f.getRawValue(row)
                    if value != groupValues[idx]:
                        groupValues[idx] = value
                        res.append(self.getHeaderRow(row, (f,) + f.outputWith))
                res.append(row)
            result = res
        for idx, row in enumerate(result):
            row.sequenceNumber = idx + 1
        return result

    @Lazy
    def result(self):
        return self.getResult()

    def __iter__(self):
        return iter(self.result)

    def first(self):
        if len(self.result) > 0:
            return self.result[0]
        return self.rowFactory(None, self)

    @Lazy
    def displayedColumns(self):
        return self.context.getActiveOutputFields()

    @Lazy
    def groupColumns(self):
        return self.context.getGroupFields()
