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


class ResultSet(object):

    def __init__(self, context, data, rowFactory=Row, headerRowFactory=Row,
                 sortCriteria=None, queryCriteria=BaseQueryCriteria(),
                 filterDublicate=False):
        self.context = context  # the report or report instance
        self.data = data
        self.rowFactory = rowFactory
        self.headerRowFactory = headerRowFactory
        self.sortCriteria = sortCriteria
        self.queryCriteria = queryCriteria
        self.filterDublicate = filterDublicate
        self.totals = BaseRow(None, self)

    def insertHeaderRow(self, idx, result):
        result.insert(idx, self.headerRowFactory(result[idx].context, self))

    def getResult(self):
        result = [self.rowFactory(item, self) for item in self.data]
        result = [row for row in result if self.queryCriteria.check(row)]
        if self.sortCriteria:
            result.sort(key=lambda x: [f.getSortValue(x) for f in self.sortCriteria])
        if self.hasGroupColumns:
            for idx, row in enumerate(result):
                insert = False
                for f in self.groupColumns:
                    if idx == 0:
                        insert = True
                    else:
                        if result[idx].getRawValue(f.name) != result[idx-1].getRawValue(f.name):
                            insert = True
                if insert:
                    self.insertHeaderRow(idx, result)
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
    
    @Lazy
    def hasGroupColumns(self):
        return len(self.groupColumns) > 0


class CombinedResultSet(ResultSet):
    
    def __init__(self, context, categorySet, resultSet):
        self.context = context
        self.categorySet = categorySet
        self.resultSet = resultSet
        self.totals = BaseRow(None, self)
    
    def getResult(self):
        result = []
        for row in self.categorySet:
            result.append(row)
            for res in self.resultSet:
                for f in self.categoryColumns:
                    if res.getRawValue(f.__name__) == row.getRawValue(f.__name__):
                        result.append(res)
        return result
    