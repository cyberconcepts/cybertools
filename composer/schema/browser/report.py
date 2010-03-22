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
from cybertools.composer.schema.browser.schema import FormManagerView
from cybertools.stateful.interfaces import IStateful


class RegistrationsExportCsv(FormManagerView):

    encoding = 'ISO8859-15'
    #delimiter = ';'
    delimiter = ','

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

    def getAllDataInColumns(self):
        """ Yield all data available, with
            columns for all data fields of all data templates.
        """
        withTemporary = self.request.get('with_temporary')
        context = self.context
        schemas = [s for s in context.getClientSchemas() if ISchema.providedBy(s)]
        headline = (['Client ID', 'Time Stamp']
             #+ list(itertools.chain(*[[self.encode(f.title)
             + list(itertools.chain(*[[self.encode(f.name)
                                            for f in s.fields
                                            if f.storeData]
                                                    for s in schemas])))
        lines = []
        clients = context.getClients()
        for name, client in clients.items():
            timeStamp = client.timeStamp
            line = [name, timeStamp]
            for schema in schemas:
                instance = IInstance(client)
                instance.template = schema
                data = instance.applyTemplate()
                for f in schema.fields:
                    if f.storeData:
                        line.append(self.encode(data.get(f.name, '')))
            lines.append(line)
        lines.sort(key=lambda x: x[1])
        for l in lines:
            l[1] = self.getFormattedDate(l[1], type='dateTime', variant='short')
        return [headline] + lines

    def render(self):
        delimiter = self.delimiter
        xlsv = self.request.form.get('xlsv')
        if xlsv == '2007':
            delimiter = ';'
        methodName = self.request.get('get_data_method', 'getAllDataInColumns')
        method = getattr(self, methodName, self.getAllDataInColumns)
        output = StringIO()
        try:
            csv.writer(output, dialect='excel', delimiter=delimiter,
                       quoting=csv.QUOTE_NONNUMERIC).writerows(method())
        except:
            import traceback; traceback.print_exc()
            raise
        result = output.getvalue()
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
