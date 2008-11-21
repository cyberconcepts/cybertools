#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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

$Id$
"""

from zope import component
from zope.interface import implements
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
import zope.schema

from cybertools.composer.schema.factory import createField
from cybertools.composer.schema.field import ListFieldInstance
from cybertools.composer.schema.interfaces import IField, IFieldInstance
from cybertools.composer.schema.interfaces import fieldTypes, undefined
from cybertools.util.format import toStr, toUnicode
from cybertools.util import json


class GridFieldInstance(ListFieldInstance):

    @Lazy
    def columnTypes(self):
        return [createField(t) for t in self.context.baseField.column_types]

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
        # TODO: marshall values!
        v = value or []
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
                row.append(fi.display(item[fi.name]))
            rows.append(row)
        return dict(headers=headers, rows=rows)

    def unmarshall(self, value):
        if not value:
            return []
        result = []
        rows = json.loads(value)['items']
        for row in rows:
            item = {}
            for fi in self.columnFieldInstances:
                item[fi.name] = fi.unmarshall(row[fi.name])
            result.append(item)
        return result