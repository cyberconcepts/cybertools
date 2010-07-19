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
Basic classes for report management.

$Id$
"""

import operator
from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.report import field
from cybertools.composer.report.interfaces import IReportManager, IReport
from cybertools.composer.report.interfaces import IQueryCriteria, ILeafQueryCriteria
from cybertools.composer.report.interfaces import ICompoundQueryCriteria
from cybertools.util.jeep import Jeep
from cybertools.util.randomname import generateName


class ReportManager(object):

    implements(IReportManager)

    reports = manager = None
    reportsFactory = dict

    def getManager(self):
        return self.manager

    def addReport(self, report):
        if self.reports is None:
            self.reports = self.reportsFactory()
        id = report.identifier
        if not id:
            id = generateName(self.checkId)
            report.identifier = id
        self.reports[id] = report
        report.manager = self
        return report

    def checkId(self, id):
        return id not in self.reports.keys()

    def getReport(self, id):
        if self.reports is None:
            return None
        return self.reports.get(id)


class Report(Template):

    implements(IReport)

    name = identifier = title = description = u''
    type = 'generic'
    manager = None

    fields = Jeep((field.label,))
    defaultOutputFields = (field.label,)
    defaultSortCriteria = (field.label,)
    presentationFormat = None

    renderers = ()
    queryCriteria = None
    outputFields = ()
    sortCriteria = ()


    def __init__(self, name):
        self.name = name

    @property
    def components(self):
        return self.fields

    def getQueryFields(self, include=None, exclude=None):
        result = [f for f in self.fields if 'query' in f.executionSteps]
        if include:
            result = [f for f in result if f.fieldType in include]
        if exclude:
            result = [f for f in result if f.fieldType not in exclude]
        return result

    def getOutputFields(self):
        return [f for f in self.fields if 'output' in f.executionSteps]

    def getActiveOutputFields(self):
        if not self.outputFields:
            fieldNames = [f.name for f in self.getOutputFields()]
            return [f for f in self.defaultOutputFields
                      if f.name in fieldNames]
        return self.outputFields

    def getAvailableOutputFields(self):
        activeNames = [f.name for f in self.getActiveOutputFields()]
        return [f for f in self.getOutputFields()
                  if f.name not in activeNames]

    def getSortFields(self):
        return [f for f in self.fields if 'sort' in f.executionSteps]

    def getSortCriteria(self):
        if not self.sortCriteria:
            fieldNames = [f.name for f in self.getSortFields()]
            return [f for f in self.defaultSortCriteria
                      if f.name in fieldNames]
        return self.sortCriteria

    def getAvailableSortFields(self):
        sortCriteria = [f.name for f in self.getSortCriteria()]
        return [f for f in self.getSortFields() if f.name not in sortCriteria]

    def getPresentationFormats(self):
        return [dict(renderer='default', title='Default')]


class BaseQueryCriteria(Component):

    implements(IQueryCriteria)

    def check(self, obj):
        return True


class LeafQueryCriteria(BaseQueryCriteria, Element):

    implements(ILeafQueryCriteria)

    def __init__(self, name, operator, comparisonValue, field):
        self.name = name
        self.operator = operator
        self.comparisonValue = comparisonValue
        self.field = field

    def check(self, row):
        if not self.comparisonValue:
            return True
        value = self.field.getSelectValue(row)
        if self.operator == 'in':
            if isinstance(value, (list, tuple)):
                for v in value:
                    if v in self.comparisonValue:
                        return True
                else:
                    return False
            else:
                return value in self.comparisonValue
        op = getattr(operator, self.operator, None)
        if op is None:
            # TODO: log warning
            return True
        #print '***', self.field.name, value, op, self.comparisonValue
        return op(value, self.comparisonValue)


class CompoundQueryCriteria(BaseQueryCriteria, Compound):

    implements(ICompoundQueryCriteria)

    logicalOperator = 'and'

    def __init__(self, parts):
        self.parts = Jeep(parts)

    def check(self, obj):
        for p in self.parts:
            if not p.check(obj):
                return False
        return True
