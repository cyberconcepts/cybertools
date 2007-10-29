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
Schema fields and related classes.

$Id$
"""

from zope.interface import implements
from zope.component import adapts
from zope import component

from cybertools.composer.base import Component
from cybertools.composer.schema.interfaces import IField, IFieldInstance
from cybertools.composer.schema.interfaces import fieldTypes
from cybertools.composer.schema.schema import formErrors
from cybertools.util.format import toStr, toUnicode


class Field(Component):

    implements(IField)

    required = False
    readonly = False
    nostore = False
    standardFieldName = None
    vocabulary = None
    renderFactory = None
    default = None

    def __init__(self, name, title=None, fieldType='textline', **kw):
        assert name
        self.__name__ = name
        title = title or u''
        self.fieldType = fieldType
        super(Field, self).__init__(title, __name__=name, **kw)
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self.__name__

    def getDefaultValue(self):
        if callable(self.default):
            return self.default()
        return self.default
    def setDefaultValue(self, value):
        self.default = value
    defaultValue = property(getDefaultValue, setDefaultValue)

    @property
    def fieldRenderer(self):
        return self.getFieldTypeInfo().fieldRenderer

    @property
    def inputRenderer(self):
        return self.getFieldTypeInfo().inputRenderer

    @property
    def storeData(self):
        return not self.nostore and self.getFieldTypeInfo().storeData

    def getTitleValue(self):
        return self.title or self.name

    def getVocabularyItems(self):
        voc = (self.vocabulary or '')
        if isinstance(voc, basestring):
            voc = voc.splitlines()
            return [dict(token=t, title=t) for t in voc if t.strip()]
        else:
            return [dict(token=t.token, title=t.title or t.value) for t in voc]

    def getFieldTypeInfo(self):
        return fieldTypes.getTerm(self.fieldType)

    def getFieldInstance(self, clientInstance=None):
        instanceName = self.getFieldTypeInfo().instanceName
        fi = component.getAdapter(self, IFieldInstance, name=instanceName)
        fi.clientInstance = clientInstance
        return fi


class FieldInstance(object):

    implements(IFieldInstance)
    adapts(IField)

    def __init__(self, context):
        self.context = context
        self.name = self.__name__ = context.name
        self.errors = []
        self.severity = 0
        self.change = None

    def marshall(self, value):
        return value or u''
        #return toStr(value)

    def display(self, value):
        return value
        #return toStr(value)

    def unmarshall(self, value):
        return toUnicode(value) or u''

    def validate(self, value, data=None):
        if not value and self.context.required:
            self.setError('required_missing')

    def setError(self, errorName, formErrors=formErrors):
        error = formErrors[errorName]
        self.errors.append(error)
        self.severity = max(error.severity, self.severity)


class NumberFieldInstance(FieldInstance):

    def marshall(self, value):
        if value is None:
            return ''
        return str(value)

    def display(self, value):
        if value is None:
            return ''
        return str(value)

    def unmarshall(self, value):
        if not value:
            return None
        return int(value)

    def validate(self, value, data=None):
        if value in ('', None):
            if self.context.required:
                self.setError('required_missing')
        else:
            try:
                int(value)
            except (TypeError, ValueError):
                self.setError('invalid_number')


class FileUploadFieldInstance(FieldInstance):

    def marshall(self, value):
        return value

    def unmarshall(self, value):
        return value


class CalculatedFieldInstance(FieldInstance):

    def marshall(self, value):
        return str(value)
