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
Message instance and related classes.

$Id$
"""

from string import Template
from zope import component
from zope.interface import implements

from cybertools.composer.instance import Instance
from cybertools.composer.interfaces import IInstance


class MessageInstance(Instance):

    template = client = None

    def __init__(self, client, template):
        self.client = client
        self.template = template

    def applyTemplate(self, **kw):
        data = DataProvider(self)
        return MessageTemplate(self.template.text).safe_substitute(data)


class DataProvider(object):

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        client = self.context.client
        messageManager = self.context.template.manager
        if key.startswith('@@'):
            viewName = key[2:]
            if client is None:
                return '$' + key
            view = component.getMultiAdapter(
                    (client.manager, TestRequest(form=form)), name=viewName)
            return view()
        elif key in messageManager.messages:
            #mi = component.getMultiAdapter(
            #       (client, messageManager.messages[key]), IInstance)
            mi = MessageInstance(client, messageManager.messages[key])
            return mi.applyTemplate()
        elif '.' in key:
            if client is None:
                return '$' + key
            schemaName, fieldName = key.split('.', 1)
            schema = client.manager.clientSchemas[schemaName]
            instance = IInstance(client)
            instance.template = schema
            data = instance.applyTemplate()
            return data[fieldName]
        else:
            raise KeyError(key)


class MessageTemplate(Template):

    idpattern = r'@{0,2}[_a-z][_.a-z0-9]*[_a-z0-9]+'
