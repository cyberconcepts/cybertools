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
Instance adapter classes for schemas.

$Id$
"""

from BTrees.OOBTree import OOBTree
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import implements, Interface

from cybertools.composer.instance import Instance as BaseInstance
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClient
from cybertools.composer.schema.schema import FormState
from cybertools.util.jeep import Jeep


class Instance(BaseInstance):

    implements(IInstance)
    adapts(Interface)

    aspect = 'schema.editor.default'
    template = None
    view = None

    def applyTemplate(self, *args, **kw):
        result = {}
        mode = kw.get('mode', 'view')
        template = self.template
        if template is not None:
            for f in template.components:
                if not f.storeData:
                    # a dummy field, e.g. a spacer
                    continue
                fi = f.getFieldInstance(self)
                name = f.name
                value = getattr(self.context, name) or fi.default
                if mode in ('view', 'preview'):
                    value = fi.display(value)
                else:
                    value = fi.marshall(value)
                result[name] = value
        return result

    def getFieldInstances(self):
        fieldInstances = Jeep()
        template = self.template
        if template is not None:
            for f in template.components:
                fieldInstances[f.name] = f.getFieldInstance(self)
        return fieldInstances

    @Lazy
    def fieldInstances(self):
        return self.getFieldInstances()


class Editor(BaseInstance):

    implements(IInstance)
    adapts(Interface)

    aspect = 'schema.editor.default'
    template = None

    def applyTemplate(self, data={}, *args, **kw):
        fieldHandlers = kw.get('fieldHandlers', {})
        ignoreValidation = kw.get('ignoreValidation', False)
        template = self.template
        context = self.context
        formState = self.validate(data)
        if template is None:
            return formState
        if formState.severity > 0 and not ignoreValidation:
            # don't do anything if there is an error
            return formState
        for f in template.components:
            if not f.storeData or f.readonly:
                # a dummy field, e.g. a spacer
                continue
            name = f.name
            ftype = f.fieldType
            fi = formState.fieldInstances[name]
            #rawValue = data.get(name, u'')
            rawValue = fi.getRawValue(data, name, u'')
            value = fi.unmarshall(rawValue)
            if ftype in fieldHandlers:  # caller wants special treatment of field
                fieldHandlers[ftype](context, value, fi, formState)
            else:
                oldValue = getattr(context, name, None)
                if value != oldValue:
                    setattr(context, name, value)
                    fi.change = (oldValue, value)
                    formState.changed = True
        return formState

    def validate(self, data):
        formState = FormState()
        if self.template is None:
            return formState
        for f in self.template.components:
            if f.readonly:
                continue
            fi = f.getFieldInstance(self)
            #value = data.get(f.name)
            value = fi.getRawValue(data, f.name)
            fi.validate(value, data)
            formState.fieldInstances.append(fi)
            formState.severity = max(formState.severity, fi.severity)
        return formState


class ClientInstance(object):

    implements(IInstance)
    adapts(IClient)

    attrsName = '__schema_attributes__'

    template = None
    baseAspect = 'schema.client.'

    @property
    def aspect(self):
        return self.baseAspect + self.template.name

    @property
    def standardAspect(self):
        return self.baseAspect + '__standard__'

    def __init__(self, context):
        self.context = context

    def applyTemplate(self, **kw):
        """ Return a mapping of field names from self.template (a schema)
            to the corresponding values from the context object.
        """
        result = dict(__name__=self.context.__name__)
        mode = kw.get('mode', 'view')
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            return result
        template = self.template
        if template is not None:
            values = attrs.get(self.aspect, {})
            for f in template.getFields():
                if not f.storeData:
                    # a dummy field, e.g. a spacer
                    continue
                fi = f.getFieldInstance(self)
                name = f.name
                #value = values.get(name, u'')
                value = values.get(name, f.getDefaultValue())
                value = mode == 'view' and fi.display(value) or fi.marshall(value)
                result[name] = value
        # update result with standard fields:
        for k, v in attrs.get(self.standardAspect, {}).items():
            result['standard.' + k] = v
        return result


class ClientInstanceEditor(ClientInstance):

    def applyTemplate(self, data={}, **kw):
        """ Store the attributes described by self.template (a schema)
            using corresponding values from the data argument.
            Return the resulting form state (an object providing IFormState).
        """
        template = self.template
        if template is None:
            return FormState()
        ignoreValidation = kw.get('ignoreValidation', False)
        formState = self.validate(data)
        if formState.severity > 0 and not ignoreValidation:
            # don't do anything if there is an error
            return formState
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            attrs = OOBTree()
            setattr(self.context, self.attrsName, attrs)
        values = attrs.setdefault(self.aspect, OOBTree())
        for f in template.fields:
            name = f.name
            if not f.storeData:
                # a dummy field, e.g. a spacer
                continue
            if name in data:
                fi = formState.fieldInstances[name]
                if fi.severity > 0:  # never store faulty field input
                    continue
                value = fi.unmarshall(data.get(name))
                oldValue = values.get(name)
                if value != oldValue:
                    values[name] = value
                    fi.change = (oldValue, value)
                    formState.changed = True
                # update standard field if appropriate:
                standardFieldName = f.standardFieldName
                if standardFieldName:
                    standardValues = attrs.setdefault(self.standardAspect, OOBTree())
                    if value != standardValues.get(standardFieldName):
                        standardValues[standardFieldName] = value
        return formState

    def validate(self, data):
        formState = FormState()
        for f in self.template.fields:
            fi = f.getFieldInstance()
            #value = fi.unmarshall(data.get(f.name))
            value = data.get(f.name)
            fi.validate(value, data)
            formState.fieldInstances.append(fi)
            formState.severity = max(formState.severity, fi.severity)
        return formState

