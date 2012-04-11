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

from zope.cachedescriptors.property import Lazy

from cybertools.composer.interfaces import IInstance
from cybertools.composer.report.base import BaseQueryCriteria



class BaseRow(object):

    def __init__(self, context, parent):
        self.context = context
        self.parent = parent
        self.data = {}
        self.sequenceNumber = 0

    def xx__getattr__(self, attr):
        f = self.parent.context.fields[attr]
        return f.getValue(self)

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


class GroupHeaderRow(BaseRow):

    def getRawValue(self, attr):
        return self.data.get(attr, u'')


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

    def insertHeaderRow(self, idx, result, columns):
        headerRow = self.headerRowFactory(None, self)
        for c in columns:
            if c.output:
                headerRow.data[c.output] = c.getDisplayValue(result[idx])
        result.insert(idx, headerRow)

    def getResult(self):
        result = [self.rowFactory(item, self) for item in self.data]
        result = [row for row in result if self.queryCriteria.check(row)]
        if self.sortCriteria:
            result.sort(key=lambda x: [f.getSortValue(x) for f in self.sortCriteria])
        if self.groupColumns:
            for idx, row in enumerate(result):
                insert = []
                for f in self.groupColumns:
                    output = [f] + f.outputWith
                    if idx == 0:
                        insert.append(output)
                    else:
                        if (result[idx].getRawValue(f.name) !=
                                result[idx-1].getRawValue(f.name)):
                            insert.append(output)
                for output in insert:
                    self.insertHeaderRow(idx, result, output)
        for idx, row in enumerate(result):
            row.sequenceNumber = idx + 1
        return result

    def __iter__(self):
        return iter(self.getResult())

    @Lazy
    def displayedColumns(self):
        return self.context.getActiveOutputFields()

    @Lazy
    def groupColumns(self):
        return self.context.getGroupFields()

