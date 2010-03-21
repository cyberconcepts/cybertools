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

from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.report.field import Field
from cybertools.composer.report.interfaces import IReportManager, IReport
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


label = Field('label', u'Label',
                u'A short text that identifies a row for humans.')


class Report(Template):

    implements(IReport)

    name = identifier = u''
    type = 'generic'
    manager = None

    fields = Jeep((label,))

    def __init__(self, name):
        self.name = name

