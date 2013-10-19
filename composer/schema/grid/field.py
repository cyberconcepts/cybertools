#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
            fi = component.getAdapter(f, IFieldInstance, name=instanceName)
            fi.clientInstance = self.clientInstance
            fi.clientContext = self.clientContext
            fi.request = self.request
            result.append(fi)
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
        value = value or []
        cardinality = getattr(self.context, 'cardinality', None)
        for item in value:
            rows.append([fi.display(item.get(fi.name))
                            for fi in self.columnFieldInstances])
        if cardinality > len(value):
            for item in range(len(value), self.context.cardinality):
                rows.append([fi.display(fi.default) 
                                for fi in self.columnFieldInstances])
        empty = not rows or (len(rows) == 1 and not [v for v in rows[0] if v])
        return dict(headers=headers, rows=rows, empty=empty)

    def unmarshall(self, value):
        value = toUnicode(value.strip())
        if not value:
            return []
        result = []
        rows = json.loads(value)['items']
        for idx, row in enumerate(rows):
            item = self.unmarshallRow(row, idx)
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

    def unmarshallRow(self, row, idx=None):
        item = {}
        cardinality = getattr(self.context, 'cardinality', None)
        for fi in self.columnFieldInstances:
            if idx is not None:
                fi.index = idx
            value = fi.unmarshall(row.get(fi.name) or u'')
            if isinstance(value, basestring):
                value = value.strip()
            if idx < cardinality:
                item[fi.name] = value
            else:
                if fi.default is not None:
                    if value == fi.default:
                        continue
                if value:
                    item[fi.name] = value
        ignoreInCheckOnEmpty = getattr(self.context, 'ignoreInCheckOnEmpty', [])
        for k, v in item.items():
            if k not in ignoreInCheckOnEmpty and v != '__no_change__':
                return item
        return {}


class RecordsFieldInstance(GridFieldInstance):

    def getRenderer(self, name):
        return grid_macros.macros.get(name)

    def marshall(self, value):
        result = []
        value = value or []
        cardinality = getattr(self.context, 'cardinality', None)
        for row in value:
            item = {}
            for fi in self.columnFieldInstances:
                item[fi.name] = fi.marshall(row.get(fi.name))
            result.append(item)
        if cardinality > len(value):
            for row in range(len(value), cardinality):
                item = {}
                for fi in self.columnFieldInstances:
                    item[fi.name] = fi.marshall(fi.default)
                result.append(item)
        return result

    def unmarshall(self, value):
        if not value:
            value = []
        result = []
        oldValue = getattr(self.clientContext, self.name, None) or []
        for idx, row in enumerate(value):
            item = self.unmarshallRow(row, idx)
            if item:
                oldItem = {}
                if len(oldValue) > idx:
                    oldItem = oldValue[idx]
                for k, v in item.items():
                    if v == '__no_change__':
                        if k in oldItem:
                            item[k] = oldItem[k]
                        else:
                            del item[k]
                if item:
                    result.append(item)
        return result

    def validate(self, value, data=None):
        if not value:
            if self.context.required:
                self.setError('required_missing')
            else:
                return
        for row in value:
            for fi in self.columnFieldInstances:
                fi.validate(row.get(fi.name) or u'')


class KeyTableFieldInstance(RecordsFieldInstance):

    @Lazy
    def keyName(self):
        return self.columnTypes[0].name

    @Lazy
    def dataNames(self):
        return [f.name for f in self.columnTypes[1:]]

    def display(self, value):
        headers = [fi.context.title for fi in self.columnFieldInstances]
        rows = []
        if value is None:
            value = {}
        for k, v in value.items():
            row = [k]
            for idx, fi in enumerate(self.columnFieldInstances[1:]):
                row.append(fi.display(v[idx]))
            rows.append(row)
        return dict(headers=headers, rows=rows)

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
        for idx, row in enumerate(value):
            item = self.unmarshallRow(row, idx)
            if item:
                result[item.pop(self.keyName)] = [item.get(name) or u''
                                                  for name in self.dataNames]
        return result


class ContextBasedKeyTableFieldInstance(KeyTableFieldInstance):

    @Lazy
    def columnTypes(self):
        obj = self.clientInstance.context
        return [Field(name) for name in obj.columnNames]

