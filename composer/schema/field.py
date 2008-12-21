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
Schema fields and related classes.

$Id$
"""

from datetime import datetime
from logging import getLogger
from time import strptime, strftime
from zope.interface import implements
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope import component
from zope.i18n.format import DateTimeParseError
from zope.i18n.locales import locales

from cybertools.composer.base import Component
from cybertools.composer.schema.interfaces import IField, IFieldInstance
from cybertools.composer.schema.interfaces import fieldTypes, undefined
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
    default_method = None
    value_type = None

    fieldTypeInfo = None
    instance_name = None
    display_renderer = None
    display_format = None


    def __init__(self, name, title=None, fieldType='textline', **kw):
        assert name
        self.__name__ = name
        #title = title or u''
        title = title or name
        self.fieldType = fieldType
        super(Field, self).__init__(title, __name__=name, **kw)
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self.__name__

    def getDefaultValue(self):
        if callable(self.default_method):
            return self.default_method()
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
    def displayRenderer(self):
        return self.display_renderer or self.getFieldTypeInfo().displayRenderer

    @property
    def storeData(self):
        return not self.nostore and self.getFieldTypeInfo().storeData

    @property
    def required_js(self):
        return self.required and 'true' or 'false'

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
        return self.fieldTypeInfo or fieldTypes.getTerm(self.fieldType)

    def getFieldInstance(self, clientInstance=None):
        instanceName = self.instance_name or self.getFieldTypeInfo().instanceName
        fi = component.getAdapter(self, IFieldInstance, name=instanceName)
        fi.clientInstance = clientInstance
        return fi


class FieldInstance(object):

    implements(IFieldInstance)
    adapts(IField)

    clientInstance = None
    value = undefined

    def __init__(self, context):
        self.context = context
        self.name = self.__name__ = context.name
        self.errors = []
        self.severity = 0
        self.change = None

    @property
    def default(self):
        dm = self.context.default_method
        if dm and isinstance(dm, str) and self.clientInstance:
            method = getattr(self.clientInstance.context, dm, None)
            if method:
                return method()
        return self.context.defaultValue

    def getRawValue(self, data, key, default=None):
        return data.get(key, default)

    def marshall(self, value):
        return value or u''
        #return toStr(value)

    def display(self, value):
        return value or u''
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
        try:
            return int(value)
        except (TypeError, ValueError):
            return float(value)

    def validate(self, value, data=None):
        if value in ('', None):
            if self.context.required:
                self.setError('required_missing')
        else:
            try:
                self.unmarshall(value)
            except (TypeError, ValueError):
                self.setError('invalid_number')


class DateFieldInstance(NumberFieldInstance):

    def marshall(self, value):
        if value is None:
            return ''
        return strftime('%Y-%m-%dT%H:%M', value.timetuple())

    def display(self, value):
        if value is None:
            return ''
        view = self.clientInstance.view
        langInfo = view and getattr(view, 'languageInfo', None) or None
        format = self.context.display_format or ('dateTime', 'short')
        if langInfo:
            locale = locales.getLocale(langInfo.language)
            fmt = locale.dates.getFormatter(*format)
            return fmt.format(value)
        return str(value)

    def unmarshall(self, value):
        if not value:
            return None
        value = ''.join(value)
        if value:
            return datetime(*(strptime(value, '%Y-%m-%dT%H:%M:%S')[:6]))
        return None

    def validate(self, value, data=None):
        if value in ('', ['', ''], None):
            if self.context.required:
                self.setError('required_missing')
        else:
            try:
                self.unmarshall(value)
            except (TypeError, ValueError, DateTimeParseError), e:
                #print '*** invalid_datetime:', value, e
                getLogger('cybertools').warn(
                        'DateFieldInstance: invalid datetime: %s, %s' % (value, e))
                self.setError('invalid_datetime')


class FileUploadFieldInstance(FieldInstance):

    def marshall(self, value):
        return value

    def unmarshall(self, value):
        return value


class EmailFieldInstance(FieldInstance):

    def validate(self, value, data=None):
        if value and '@' not in value:
            self.setError('invalid_email_address')


class BooleanFieldInstance(FieldInstance):

    def marshall(self, value):
        return value

    def display(self, value):
        #return value and _(u'Yes') or _(u'No')
        return value and u'X' or u'-'

    def unmarshall(self, value):
        return bool(value)


class CalculatedFieldInstance(FieldInstance):

    def marshall(self, value):
        return str(value)


class ListFieldInstance(FieldInstance):

    @Lazy
    def valueType(self):
        return self.context.value_type

    @Lazy
    def valueFieldInstance(self):
        if self.valueType is None:
            return FieldInstance(self.context)
        else:
            instanceName = (self.valueType.instance_name or
                            self.valueType.getFieldTypeInfo().instanceName)
        return component.getAdapter(self.valueType, IFieldInstance, name=instanceName)

    def marshall(self, value):
        if isinstance(value, basestring):
            return value
        return u'\n'.join(self.valueFieldInstance.marshall(v) for v in value)
        #return [self.valueFieldInstance.marshall(v) for v in value]

    def display(self, value):
        if isinstance(value, basestring):
            return value
        return u' | '.join(self.valueFieldInstance.display(v) for v in value)

    def unmarshall(self, value):
        if isinstance(value, basestring):
            value = value.split('\n')
        return [self.valueFieldInstance.unmarshall(v.strip())
                        for v in value if v.strip()]

