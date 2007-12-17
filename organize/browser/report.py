#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
View classes for CSV export.

$Id$
"""

import csv
from cStringIO import StringIO
from zope import component
from zope.cachedescriptors.property import Lazy
from cybertools.composer.interfaces import IInstance
from cybertools.stateful.interfaces import IStateful


class RegistrationsExportCsv(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def setHeaders(self, size, filename=None):
        filename = filename or 'registrations.csv'
        response = self.request.response
        response.setHeader('Content-Disposition',
                           'attachment; filename=%s' % filename)
        response.setHeader('Content-Type', 'text/x-comma-separated-values')
        response.setHeader('Content-Length', size)

    def getData(self):
        withTemporary = self.request.get('with_temporary')
        yield ['Service', 'Client ID', 'Organization', 'First Name', 'Last Name', 'E-Mail',
               'Number', 'State']
        for service in self.context.getServices():
            for clientName, reg in service.registrations.items():
                client = reg.client
                data = IInstance(client).applyTemplate()
                state = IStateful(reg).getStateObject()
                if state.name == 'temporary' and not withTemporary:
                    continue
                yield [encode(service.title) or service.name,
                       clientName,
                       encode(data.get('standard.organization', '')),
                       encode(data.get('standard.lastName', '')),
                       encode(data.get('standard.firstName', '')),
                       encode(data.get('standard.email', '')),
                       reg.number,
                       state.title
                ]

    def render(self):
        output = StringIO()
        csv.writer(output).writerows(self.getData())
        result = output.getvalue()
        self.setHeaders(len(result))
        return result

    def render2(self):
        # using cybertools.reporter.resultset
        rs = self.getData()     # returns a ResultSet
        result = rs.asCsv()
        self.setHeaders(len(result))
        return result


def encode(text, encoding='UTF-8'):
    if type(text) is unicode:
        text = text.encode(encoding)
    return text
