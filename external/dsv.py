#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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


class CsvReader(BaseReader):

    elementFactories = {None: Element}
    fieldNames = ()
    start = stop = None

    def read(self, input):
        result = []
        reader = csv.DictReader(input, self.fieldNames)
        lastIdentifiers = {}
        for idx, row in enumerate(list(reader)[self.start:self.stop]):
            currentElements = {}
            for k, v in row.items():
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
                    element = currentElements[type] = ef()
                    element.type = type
                element[k] = v      # ?TODO: unmarshall
            for element in sorted(currentElements.values(), key=lambda x: x.order):
                id = element.identifier
                if not id or id != lastIdentifiers.get(element.type):
                    element.setParent(currentElements)
                    result.append(element)
                    lastIdentifiers[element.type] = id
        return result

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
