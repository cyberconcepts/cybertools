#
#  Copyright (c) 2011 Helmut Merz helmutm@cy55.de
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
"""

import operator as standard_operators
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

    name = identifier = u''
    #title = description = u''
    type = 'generic'
    manager = None

    fields = Jeep((field.label,))
    hiddenQueryFields = ()
    userSettings = (field.label,)
    defaultOutputFields = (field.label,)
    defaultSortCriteria = (field.label,)
    presentationFormat = None

    renderers = ()
    queryCriteria = None
    outputFields = ()
    sortCriteria = ()
    sortDescending = False
    limits = None


    def __init__(self, name):
        self.name = name

    @property
    def components(self):
        return self.fields

    def getAllQueryFields(self):
        return [f for f in self.fields if 'query' in f.executionSteps]

    def getQueryFields(self, include=None, exclude=None):
        result = [f for f in self.fields if 'query' in f.executionSteps]
        if include:
            result = [f for f in result if f.fieldType in include]
        if exclude:
            result = [f for f in result if f.fieldType not in exclude]
        return [f for f in result if f not in self.hiddenQueryFields]

    def getOutputFields(self):
        return [f for f in self.fields if 'output' in f.executionSteps]

    def getAllFields(self):
        return [f for f in self.fields]

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

    def getGroupFields(self):
        return [f for f in self.fields if 'group' in f.executionSteps]

    def getTotalsFields(self):
        return [f for f in self.fields if 'totals' in f.executionSteps]

    def getSubTotalsFields(self):
        result = []
        for gf in self.getGroupFields():
            result.append([f for f in self.fields if gf.name in f.totals])
        return result

    def getSubTotalsGroupFields(self):
        result = []
        for f in self.fields:
            result.extend(gf for gf in self.getGroupFields() if gf.name in f.totals)
        return result

    def getOutputFieldsForField(self, field):
        return [f for f in self.fields if f.name == field.output]


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
        comparisonValue = self.comparisonValue
        if comparisonValue in (None, '',):
            comparisonValue = self.field.defaultComparisonValue
            if comparisonValue in (None, '',):
                return True
        value = self.field.getSelectValue(row)
        if (self.field.fieldType == 'number' and
                isinstance(comparisonValue, basestring)):
            comparisonValue = int(comparisonValue)
        op = operators.get(self.operator)
        if op is None:
            op = getattr(standard_operators, self.operator, None)
        if op is None:
            # TODO: log warning
            return True
        return op(value, comparisonValue)

    def showComparisonValue(self):
        if self.field.fieldType == 'selection' and self.comparisonValue:
            return ', '.join([v for v in self.comparisonValue])
        return self.comparisonValue

    def showOperator(self):
        op = self.operator
        for item in self.field.operators:
            if item['token'] == op:
                return item['label']
        return op


def checkOnly(value, compValue):
    if not value:
        return 'none' in compValue
    for v in value:
        if v not in compValue:
            return False
    return True

def checkIn(value, compValue):
    return value in compValue

def checkAny(value, compValue):
    for v in value:
        if v in compValue:
            return True
    return False

def checkNotAny(value, compValue):
    return not checkAny(value, compValue)

operators = {'any': checkAny, 'not_any': checkNotAny,
             'in': checkIn, 'only': checkOnly}


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
