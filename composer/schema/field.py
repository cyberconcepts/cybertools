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
Schema fields and related classes.
"""

from datetime import datetime
from logging import getLogger
from time import strptime, strftime
from zope.app.form.browser.interfaces import ITerms
from zope.i18n.locales import locales
from zope.interface import implements
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope import component
from zope.i18n.format import DateTimeParseError
from zope.i18n.locales import locales
from zope.schema.interfaces import IVocabularyFactory, IContextSourceBinder
from zope.tales.engine import Engine
from zope.tales.tales import Context

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
    showEmpty = False
    standardFieldName = None
    vocabulary = None
    renderFactory = None
    default = None
    default_method = None
    defaultValueType = 'static'

    value_type = None

    fieldTypeInfo = None
    baseField = None
    instance_name = None
    input_renderer = None
    display_renderer = None
    display_format = None


    def __init__(self, name, title=None, fieldType='textline', **kw):
        assert name
        self.__name__ = name
        #title = title or u''
        title = title or name
        self.fieldType = fieldType
        #super(Field, self).__init__(title, __name__=name, **kw)
        self.title = title
        for k, v in kw.items():
            setattr(self, k, v)

    def __getattr__(self, attr):
        if self.baseField is not None:
            return getattr(self.baseField, attr)
        raise AttributeError(attr)

    @property
    def name(self):
        return self.__name__

    def getDefaultValue(self):
        if callable(self.default_method):
            return self.default_method()
        if self.defaultValueType == 'tales':
            expr = Engine.compile(self.default)
            ctx = Context(Engine, self.getContextProperties())
            try:
                return expr(ctx)
            except AttributeError, KeyError:
                return u''
        return self.default
    def setDefaultValue(self, value):
        self.default = value
    defaultValue = property(getDefaultValue, setDefaultValue)

    def getDefaultValueExpr(self):
        return self.default
    def setDefaultValueExpr(self, value):
        self.default = value
    defaultValueExpr = property(getDefaultValueExpr, setDefaultValueExpr)

    @property
    def fieldRenderer(self):
        return self.getFieldTypeInfo().fieldRenderer

    @property
    def inputRenderer(self):
        return self.input_renderer or self.getFieldTypeInfo().inputRenderer

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

    def getVocabularyItems(self, instance=None, request=None):
        context = None
        if instance is not None:
            context = instance.context
        voc = (self.vocabulary or '')
        if isinstance(voc, basestring):
            terms = self.getVocabularyTerms(voc, context, request)
            if terms is not None:
                return terms
            voc = voc.splitlines()
            return [dict(token=t, title=t) for t in voc if t.strip()]
        elif IContextSourceBinder.providedBy(voc):
            source = voc(instance)
            terms = component.queryMultiAdapter((source, request), ITerms)
            if terms is not None:
                termsList = [terms.getTerm(value) for value in source]
                return [dict(token=t.token, title=t.title) for t in termsList]
            else:
                return None
        return [dict(token=t.token, title=t.title or t.value) for t in voc]

    def getVocabularyTerms(self, name, context, request):
        if context is None or request is None:
            return None
        source = component.queryUtility(IVocabularyFactory, name=name)
        if source is not None:
            source = source(context)
            terms = component.queryMultiAdapter((source, request), ITerms)
            if terms is not None:
                termsList = [terms.getTerm(value) for value in source]
                return [dict(token=t.token, title=t.title) for t in termsList]
        return None

    def getFieldTypeInfo(self):
        return self.fieldTypeInfo or fieldTypes.getTerm(self.fieldType)

    def getFieldInstance(self, clientInstance=None, context=None, request=None):
        instanceName = self.instance_name or self.getFieldTypeInfo().instanceName
        fi = component.queryAdapter(self, IFieldInstance, name=instanceName)
        if fi is None:
            fi = component.getAdapter(self, IFieldInstance, name='')
        fi.clientInstance = clientInstance
        fi.clientContext = context
        fi.request = request
        return fi

    def getContextProperties(self):
        return dict(context=self, user=None)


class FieldInstance(object):

    implements(IFieldInstance)
    adapts(IField)

    clientInstance = None
    clientContext = None
    value = undefined
    request = None
    index = None

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
        return self.context.getDefaultValue()

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

    def getRenderer(self, name):
        return None


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
            #return int(str(value))
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


class DecimalFieldInstance(NumberFieldInstance):

    format = 'decimal'

    def marshall(self, value):
        return self.display(value, pattern=u'0.00;-0.00')

    def display(self, value, pattern=u'#,##0.00;-#,##0.00'):
        if value is None:
            return ''
        if isinstance(value, basestring):
            if not value.isdigit():
                return value
            value = float(value)
        view = self.clientInstance.view
        langInfo = view and getattr(view, 'languageInfo', None) or None
        if langInfo:
            locale = locales.getLocale(langInfo.language)
            fmt = locale.numbers.getFormatter(self.format)
            return fmt.format(value, pattern=pattern)
        return '%.2f' % value

    def unmarshall(self, value):
        if not value:
            return None
        if ',' in value:
            value = value.replace(',', '.')
        return float(value)


class DateFieldInstance(NumberFieldInstance):

    def marshall(self, value):
        if not value:
            return ''
        if isinstance(value, basestring):
            return value
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
        if len(value) > 1 and value[0] and not value[1]:
            value[1] = 'T00:00:00'
        value = ''.join(value)
        if value:
            try:
                return datetime(*(strptime(value, '%Y-%m-%dT%H:%M:%S')[:6]))
            except ValueError:
                try:
                    return datetime(*(strptime(value, '%Y-%m-%dT%H:%M')[:6]))
                except ValueError:
                    return datetime(*(strptime(value, '%Y-%m-%d')[:6]))
        return None

    def validate(self, value, data=None):
        if value in ('', ['', ''], None):
            if self.context.required:
                self.setError('required_missing')
        else:
            try:
                self.unmarshall(value)
            except (TypeError, ValueError, DateTimeParseError), e:
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
        if not value and self.context.required:
            self.setError('required_missing')
        if value and '@' not in value:
            self.setError('invalid_email_address')


class BooleanFieldInstance(FieldInstance):

    def marshall(self, value):
        return bool(value)

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
        if value is None:
            return u''
        return u'\n'.join(unicode(self.valueFieldInstance.marshall(v)) for v in value)
        #return [self.valueFieldInstance.marshall(v) for v in value]

    def display(self, value):
        if not value:
            return u''
        if isinstance(value, basestring):
            return value
        return u' | '.join(unicode(self.valueFieldInstance.display(v)) for v in value)

    def unmarshall(self, value):
        if isinstance(value, basestring):
            value = value.split('\n')
        return [self.valueFieldInstance.unmarshall(v.strip())
                        for v in value if v.strip()]


class CheckBoxesFieldInstance(ListFieldInstance):

    def marshal(self, value):
        return value

    def ummarshal(self, value):
        return value


class DropdownFieldInstance(FieldInstance):

    def display(self, value):
        items = self.context.getVocabularyItems(self.clientInstance, self.request)
        for item in items:
            if str(item['token']) == str(value):
                return item['title']
        return value or u''

