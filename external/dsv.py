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
Base implementation for import adapters.

$Id$
"""

import csv
from datetime import date, timedelta
from time import strptime

from zope import component
from zope.interface import implements
from zope.cachedescriptors.property import Lazy

from cybertools.external.base import BaseReader
from cybertools.external.element import Element


xls2csv = '%(cpath)s -f %%Y-%%m-%%d %(fpath)s.xls >%(fpath)s.csv'


class CsvReader(BaseReader):

    encoding = 'UTF-8'
    elementFactories = {None: Element}
    fieldNames = ()
    start = stop = sortKey = None

    def read(self, input):
        result = []
        for x in range(self.start or 0):
            input.readline()    # skip lines on top
        reader = csv.DictReader(input, self.fieldNames)
        allElements = {}
        rows = list(reader)[:self.stop]
        if self.sortKey:
            rows.sort(key=self.sortKey)
        for idx, row in enumerate(rows):
            if self.ignoreRow(idx, row):
                continue
            currentElements = {}
            for k, v in row.items():
                k, v = self.preprocessField(k, v)
                if k is None:
                    continue
                type = None
                if '.' in k:
                    type, k = k.split('.', 1)
                element = currentElements.get(type)
                if element is None:
                    ef = self.elementFactories.get(type)
                    if ef is None:
                        raise ValueError('Missing element factory for %r.' % type)
                    if ef == 'ignore':
                        continue
                    element = currentElements[type] = ef()
                    element.type = type
                if isinstance(v, str):
                    v = v.decode(self.encoding)
                element[k] = v
            for element in sorted(currentElements.values(), key=lambda x: x.order):
                if element.identifier is None:
                    result.append(element)
                    element.setParent(currentElements, allElements)
                else:
                    typeEntry = allElements.setdefault(element.type, {})
                    existing = typeEntry.get(element.identifier)
                    if existing is None:
                        typeEntry[element.identifier] = element
                        result.append(element)
                        element.setParent(currentElements, allElements)
        return result

    def ignoreRow(self, idx, row):
        return False

    def preprocessField(self, k, v):
        return k, v

    def getDate(self, value, correctBug=False):
        if not value:
            return value
        try:
            v = strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
        else:
            d = date(*v[:3])
            if correctBug:
                d -= timedelta(4 * 365 + 2)
            return d
