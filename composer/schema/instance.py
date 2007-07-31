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
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            return result
        template = self.template
        values = attrs.setdefault(self.aspect, {})
        if template is not None:
            for c in template.components:
                name = c.name
                result[name] = values.get(name, u'')
        result['__name__'] = self.context.__name__
        return result


class ClientInstanceEditor(ClientInstance):

    def applyTemplate(self, data={}, **kw):
        """ Store the attributes described by self.template (a schema)
            using corresponding values from the data argument.
        """
        attrs = getattr(self.context, self.attrsName, None)
        if attrs is None:
            attrs = OOBTree()
            setattr(self.context, self.attrsName, attrs)
        template = self.template
        values = attrs.setdefault(self.aspect, OOBTree())
        if template is not None:
            for c in template.components:
                name = c.name
                if name in data:
                    values[name] = data[name]

