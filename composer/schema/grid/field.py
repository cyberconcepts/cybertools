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
Field and field instance classes for grids.
"""

from zope import component
from zope.component import adapts
from zope.interface import implements
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
import zope.schema

from cybertools.composer.schema.factory import createField
from cybertools.composer.schema.field import Field, ListFieldInstance
from cybertools.composer.schema.interfaces import IField, IFieldInstance
from cybertools.composer.schema.interfaces import fieldTypes, undefined
from cybertools.util.format import toStr, toUnicode
from cybertools.util import json


grid_macros = ViewPageTemplateFile('grid_macros.pt')


class GridFieldInstance(ListFieldInstance):

    @Lazy
    def columnTypes(self):
        return [createField(t) for t in self.context.column_types]

    @Lazy
    def columnFieldInstances(self):
        result = []
        for f in self.columnTypes:
            instanceName = (f.instance_name or
                            f.getFieldTypeInfo().instanceName)
            result.append(component.getAdapter(f, IFieldInstance,
                                               name=instanceName))
        return result

    def marshall(self, value):
        if isinstance(value, basestring):
            return value
        v = value or []
        for row in v:
            for fi in self.columnFieldInstances:
                vr = fi.marshall(row[fi.name])
                if isinstance(vr, basestring):
                    row[fi.name] = vr.replace('\n', '\\n').replace('"', '\\"')
        empty = {}
        for fi in self.columnFieldInstances:
            default = fi.default
            if default is None:
                default = ''
            empty[fi.name] = str(default)
        for i in range(3):
            v.append(empty)
        return json.dumps(dict(items=v))

    def display(self, value):
        headers = [fi.context.title for fi in self.columnFieldInstances]
        rows = []
        for item in value or []:
            row = []
            for fi in self.columnFieldInstances:
                row.append(fi.display(item.get(fi.name)))
            rows.append(row)
        return dict(headers=headers, rows=rows)

    def unmarshall(self, value):
        value = toUnicode(value.strip())
        if not value:
            return []
        result = []
        rows = json.loads(value)['items']
        for row in rows:
            item = self.unmarshallRow(row)
            if item:
                result.append(item)
        return result

    def dummy(self):
        for row in rows:
            item = {}
            empty = True
            for fi in self.columnFieldInstances:
                value = fi.unmarshall(row[fi.name])
                item[fi.name] = value
                if fi.default is not None:
                    if value != fi.default:
                        empty = False
                elif value:
                    empty = False
            if not empty:
                result.append(item)
        return result

    def unmarshallRow(self, row):
        item = {}
        for fi in self.columnFieldInstances:
            value = fi.unmarshall(row[fi.name])
            if isinstance(value, basestring):
                value = value.strip()
            if fi.default is not None:
                if value == fi.default:
                    continue
            item[fi.name] = value
        return item


class RecordsFieldInstance(GridFieldInstance):

    def marshall(self, value):
        result = []
        for row in value or []:
            item = {}
            for fi in self.columnFieldInstances:
                item[fi.name] = fi.marshall(row.get(fi.name))
            result.append(item)
        return result

    def unmarshall(self, value):
        if not value:
            value = []
        result = []
        for row in value:
            item = self.unmarshallRow(row)
            if item:
                result.append(item)
        return result


class KeyTableFieldInstance(RecordsFieldInstance):

    @Lazy
    def keyName(self):
        return self.columnTypes[0].name

    @Lazy
    def dataNames(self):
        return [f.name for f in self.columnTypes[1:]]

    def marshall(self, value):
        result = []
        if not value:
            return result
        for k, v in value.items():
            item = {self.keyName: k}
            for idx, name in enumerate(self.dataNames):
                item[name] = v[idx]
            result.append(item)
        return result

    def unmarshall(self, value):
        if not value:
            value = {}
        result = {}
        for row in value:
            item = self.unmarshallRow(row)
            if item:
                result[item.pop(self.keyName)] = [item.get(name)
                                                  for name in self.dataNames]
        return result


class ContextBasedKeyTableFieldInstance(KeyTableFieldInstance):

    @Lazy
    def columnTypes(self):
        obj = self.clientInstance.context
        return [Field(name) for name in obj.columnNames]

