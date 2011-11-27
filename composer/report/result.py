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
Report result sets and related classes.
"""

from zope.cachedescriptors.property import Lazy

from cybertools.composer.interfaces import IInstance
from cybertools.composer.report.base import BaseQueryCriteria


def getContextAttr(obj, attr):
    return getattr(obj.context, attr)


class Row(object):

    attributeHandlers = {}

    def __init__(self, context, parent):
        self.context = context
        self.parent = parent

    def __getattr__(self, attr):
        f = self.parent.context.fields[attr]
        return f.getValue(self)

    def getRawValue(self, attr):
        return self.attributeHandlers.get(attr, getContextAttr)(self, attr)


class ResultSet(object):

    def __init__(self, context, data, rowFactory=Row,
                 sortCriteria=None, queryCriteria=BaseQueryCriteria()):
        self.context = context  # the report or report instance
        self.data = data
        self.rowFactory = rowFactory
        self.sortCriteria = sortCriteria
        self.queryCriteria = queryCriteria

    def getResult(self):
        result = [self.rowFactory(item, self) for item in self.data]
        result = [row for row in result if self.queryCriteria.check(row)]
        if self.sortCriteria:
            result.sort(key=lambda x: [f.getSortValue(x) for f in self.sortCriteria])
        return result

    def __iter__(self):
        return iter(self.getResult())

