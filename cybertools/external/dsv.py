# cybertools.external.ds

""" Base implementation for import adapters.
"""

import csv
from datetime import date, timedelta
from time import strptime

from zope import component
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
                keys, v = self.preprocessField(k, v)
                if not keys:
                    continue
                if not isinstance(keys, (tuple, list)):
                    keys = [keys]
                for k in keys:
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
                    self.setValue(element, k, v)
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

    def setValue(self, element, k, v):
        element[k] = v

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
