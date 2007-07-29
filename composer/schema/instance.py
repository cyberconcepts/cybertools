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


class ClientInstanceAdapter(object):

    implements(IInstance)
    adapts(IClient)

    baseAspect = 'schema.client.'
    schema = 'default'

    @property
    def aspect(self):
        return self.baseAspect + self.schema

    @property
    def template(self):
        return self.context.manager.clientSchemas.get(self.schema, None)

    def __init__(self, context):
        self.context = context

    def applyTemplate(self, data={}, schema='default', **kw):
        if getattr(self.context, 'attributes', None) is None:
            self.context.attributes = OOBTree()
        self.schema = schema
        template = self.template
        attributes = self.context.attributes.setdefault(self.aspect, OOBTree())
        if template is not None:
            for c in template.components:
                name = c.name
                attributes[name] = data.get(name, u'')

