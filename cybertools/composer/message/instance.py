#
#  Copyright (c) 2011 Helmut Merz helmutm@cy55.de
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

from cgi import parse_qs
from string import Template
from zope import component
from zope.interface import implements
from zope.publisher.browser import TestRequest
try:
    from zope.traversing.browser.absoluteurl import absoluteURL
    zope29 = False
except ImportError:
    from zope.app.traversing.browser.absoluteurl import absoluteURL
    from Acquisition import aq_parent, aq_inner
    zope29 = True

from cybertools.composer.instance import Instance
from cybertools.composer.interfaces import IInstance
from cybertools.util.jeep import Jeep

_not_found = object()


class DataProvider(object):

    extensions = {}

    def __init__(self, context, data):
        self.context = context
        self.data = data

    def __getitem__(self, key):
        if key in self.extensions:
            return self.extensions[key](self)
        client = self.context.client
        messageManager = self.context.manager
        if key.startswith('@@'):
            if client is None:
                return '$' + key
            viewName = key[2:]
            params = {}
            if '?' in viewName:
                viewName, params = viewName.split('?', 1)
                params = parse_qs(params)
            view = self.getView(viewName)
            if view is not None:
                view.options = params
                return view()
            else:
                return key
        elif '|' in key:
            elements = key.split('|')
            key = elements.pop(0)
            value = self[key]
            if len(elements) > 1:
                if elements[0] == value:
                    return elements[1]
                else:
                    return ''
            return value
        elif key in messageManager.messages:
            mi = MessageInstance(client, messageManager.messages[key],
                                 messageManager)
            return mi.applyTemplate(self.data)['text']
        elif '.' in key:
            return self.getSubfieldValue(key)
        elif key in self.data:
            return self.data[key]
        else:
            raise KeyError(key)

    def getView(self, name):
        request = self.data.get('request') or TestRequest()
        view = component.queryMultiAdapter(
                    (self.context.client.manager, request), name=name)
        return view

    def getSubfieldValue(self, key):
        client = self.context.client
        if client is None:
            return '$' + key
        schemaName, fieldName = key.split('.', 1)
        schema = self.getClientSchemas().get(schemaName)
        if schema is None:
            return '$' + key
        instance = IInstance(self.getSubclient(schemaName))
        instance.template = schema
        data = instance.applyTemplate()
        value = data.get(fieldName, _not_found)
        if value is _not_found:
            return '$' + key
        return value

    def getSubclient(self, name):
        return self.context.client

    def getClientSchemas(self):
        return self.context.client.manager.getClientSchemas()


class MessageInstance(Instance):

    template = client = None

    dataProvider = DataProvider

    def __init__(self, client, template, manager):
        self.client = client
        self.template = template
        self.manager = manager

    def applyTemplate(self, data=None, **kw):
        if data is None:
            data = {}
        request = data.get('request') or TestRequest()
        if 'url' not in data:
            data['url'] = self.getClientUrl(request)
        dp = self.dataProvider(self, data)
        text = MessageTemplate(self.template.text).safe_substitute(dp)
        subject = self.template.subjectLine
        data.update(dict(subjectLine=subject, text=text))
        return data

    def getClientUrl(self, request):
        if self.client is None:
            return ''
        if zope29:
            #path = aq_inner(self.client.manager).getPhysicalPath()
            path = self.client.manager.getPhysicalPath()
            if len(path) >= 3 and path[-3] == 'sm_clients':
                print '*** path correction:', path
                # evil hack for aqcuisition-wrapped manager object
                path = path[:-3]
            url = request.physicalPathToURL(path)
        else:
            url = absoluteURL(self.client.manager, request)
        return '%s?id=%s' % (url, self.client.__name__)


class MessageTemplate(Template):

    idpattern = r'@{0,2}[_a-z][_.|a-z0-9]*[_a-z0-9?&=]+'
