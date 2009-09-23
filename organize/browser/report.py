#
#  Copyright (c) 20098 Helmut Merz helmutm@cy55.de
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
import itertools
from zope import component
from zope.cachedescriptors.property import Lazy
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import ISchema
from cybertools.organize.browser.service import BaseView
from cybertools.stateful.interfaces import IStateful


class RegistrationsExportCsv(BaseView):

    encoding = 'ISO8859-15'

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
                yield [self.encode(service.title) or service.name,
                       clientName,
                       self.encode(data.get('standard.organization', '')),
                       self.encode(data.get('standard.lastName', '')),
                       self.encode(data.get('standard.firstName', '')),
                       self.encode(data.get('standard.email', '')),
                       reg.number,
                       state.title
                ]

    def getAllDataInColumns(self):
        """ Yield all data available, with a column for each service and
            columns for all data fields of all data templates.
        """
        withTemporary = self.request.get('with_temporary')
        context = self.context
        services = context.getServices()
        withWaitingList = False
        for service in services:
            if service.waitingList:
                withWaitingList = True
                break
        schemas = [s for s in context.getClientSchemas() if ISchema.providedBy(s)]
        headline = (['Client ID', 'Time Stamp']
             + list(itertools.chain(*[[self.encode(f.title)
                                            for f in s.fields]
                                                    for s in schemas])))
        for s in services:
            headline.append(self.encode(s.title))
            if withWaitingList:
                headline.append('WL ' + self.encode(s.title))
        #     + [self.encode(s.title) for s in services])
        #if withWaitingList:
        #    headline += ['WL ' + self.encode(s.title) for s in services]
        lines = []
        clients = context.getClients()
        for name, client in clients.items():
            hasRegs = False
            regs = []
            #waiting = []
            timeStamp = ''
            for service in services:
                reg = service.registrations.get(name)
                if reg is None:
                    regs.append(0)
                    if withWaitingList:
                        regs.append(0)
                    #waiting.append(0)
                else:
                    state = IStateful(reg).getStateObject()
                    if state.name == 'temporary' and not withTemporary:
                        regs.append(0)
                        if withWaitingList:
                            regs.append(0)
                        #waiting.append(0)
                    else:
                        regs.append(reg.number)
                        if withWaitingList:
                            regs.append(reg.numberWaiting)
                        #waiting.append(reg.numberWaiting)
                        if reg.number or reg.numberWaiting:
                            hasRegs = True
                        if reg.timeStamp < timeStamp:
                            timeStamp = reg.timeStamp
            if not hasRegs:
                continue
            line = [name, timeStamp]
            for schema in schemas:
                instance = IInstance(client)
                instance.template = schema
                data = instance.applyTemplate()
                for f in schema.fields:
                    line.append(self.encode(data.get(f.name, '')))
            line += regs
            #if withWaitingList:
            #    line += waiting
            lines.append(line)
        lines.sort(key=lambda x: x[1])
        for l in lines:
            l[1] = self.getFormattedDate(l[1], type='dateTime', variant='short')
        return [headline] + lines

    def render(self):
        methodName = self.request.get('get_data_method', 'getAllDataInColumns')
        method = getattr(self, methodName, self.getData)
        output = StringIO()
        try:
            csv.writer(output, dialect='excel', delimiter=';').writerows(method())
        except:
            import traceback; traceback.print_exc()
            raise
        result = output.getvalue()
        self.setHeaders(len(result))
        return result

    def render2(self):
        # using cybertools.reporter.resultset
        rs = self.getData()     # should return a ResultSet
        result = rs.asCsv()
        self.setHeaders(len(result))
        return result

    def encode(self, text):
        if type(text) is unicode:
            result = []
            for c in text:
                try:
                    c = c.encode(self.encoding)
                except UnicodeEncodeError:
                    c = '?'
                result.append(c)
            text = ''.join(result)
        return text
