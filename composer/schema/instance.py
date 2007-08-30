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
from zope.component import adapts
from zope.interface import implements

from cybertools.composer.instance import Instance
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClient
from cybertools.composer.schema.schema import FormState


class Editor(Instance):

    aspect = 'schema.editor.default'

    def applyTemplate(self, data={}, *args, **kw):
        for c in self.template.components:
            # TODO: implement the real stuff
            # save data (if available) in context
            # build sequence of fields with data from context
            # or directly use request...
            print c.name, getattr(self.context, c.name, '-')


class ClientInstance(object):

    implements(IInstance)
    adapts(IClient)

    attrsName = '__schema_attributes__'

    template = None
    baseAspect = 'schema.client.'

    @property
    def aspect(self):
        return self.baseAspect + self.template.name

    def __init__(self, context):
        self.context = context

    def applyTemplate(self, **kw):
        """ Return a mapping of field names from self.template (a schema)
            to the corresponding values from the context object.
        """
        result = {}
        mode = kw.get('mode', 'view')
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            return result
        template = self.template
        values = attrs.setdefault(self.aspect, {})
        if template is not None:
            for f in template.fields:
                fieldType = f.getFieldTypeInfo()
                if not fieldType.storeData:
                    # a dummy field, e.g. a spacer
                    continue
                fi = f.getFieldInstance()
                name = f.name
                value = values.get(name, u'')
                value = mode == 'view' and fi.display(value) or fi.marshall(value)
                result[name] = value
        result['__name__'] = self.context.__name__
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
        formState = self.validate(data)
        if formState.severity > 0:
            # don't do anything if there is an error
            return formState
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            attrs = OOBTree()
            setattr(self.context, self.attrsName, attrs)
        values = attrs.setdefault(self.aspect, OOBTree())
        for f in template.fields:
            name = f.name
            fieldType = f.getFieldTypeInfo()
            if not fieldType.storeData:
                # a dummy field, e.g. a spacer
                continue
            fi = formState.fieldInstances[name]
            value = fi.unmarshall(data.get(name))
            if name in data:
                oldValue = values.get(name)
                if value != oldValue:
                    values[name] = value
                    fi.change = (oldValue, value)
                    formState.changed = True
        return formState

    def validate(self, data):
        formState = FormState()
        for f in self.template.fields:
            fi = f.getFieldInstance()
            #value = fi.unmarshall(data.get(f.name))
            value = data.get(f.name)
            fi.validate(value)
            formState.fieldInstances.append(fi)
            formState.severity = max(formState.severity, fi.severity)
        return formState

