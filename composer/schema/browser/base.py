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
Basic browser view classes for composer.schema.

$Id$
"""

from zope import component
from zope.cachedescriptors.property import Lazy
from zope.traversing.browser import absoluteURL

from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClientFactory


class SchemaView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.clientName = None

    @Lazy
    def fields(self):
        return self.context.fields

    @Lazy
    def data(self):
        form = self.request.form
        clientName = self.clientName = form.get('id')
        if not clientName:
            return {}
        manager = self.context.manager
        client = manager.clients.get(clientName)
        if client is None:
            return {}
        instance = IInstance(client)
        instance.template = self.context
        return instance.applyTemplate()

    def update(self):
        form = self.request.form
        if not form.get('action'):
            return True
        manager = self.context.manager
        clientName = form.get('id')
        if clientName:
            client = manager.clients.get(clientName)
            if client is None:
                # TODO: provide error message (?)
                return True
        else:
            client = IClientFactory(manager)()
            clientName = self.clientName = manager.addClient(client)
        instance = component.getAdapter(client, IInstance, name='editor')
        instance.template = self.context
        instance.applyTemplate(form)
        self.request.response.redirect(self.nextUrl)
        return False

    @Lazy
    def nextUrl(self):
        url = absoluteURL(self.context, self.request)
        return '%s/thank_you?id=%s' % (url, self.clientName)
