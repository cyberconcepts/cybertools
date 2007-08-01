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

from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClientFactory


class SchemaView(object):

    clientName = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def fields(self):
        return self.context.fields

    @Lazy
    def data(self):
        return self.getData()

    def getData(self):
        if not self.clientName:
            form = self.request.form
            self.clientName = form.get('id')
        clientName = self.clientName
        if not clientName:
            return {}
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return {}
        instance = IInstance(client)
        instance.template = self.context
        return instance.applyTemplate()

    def update(self):
        form = self.request.form
        if not self.clientName:
            self.clientName = form.get('id')
        clientName = self.clientName
        if not form.get('action'):
            return True
        manager = self.context.getManager()
        if clientName:
            client = manager.getClients().get(clientName)
            if client is None:
                return True
        else:
            client = IClientFactory(manager)()
            clientName = self.clientName = manager.addClient(client)
        instance = component.getAdapter(client, IInstance, name='editor')
        instance.template = self.context
        instance.applyTemplate(form)
        return True
        #self.request.response.redirect(self.nextUrl)
        #return False

    @Lazy
    def nextUrl(self):
        from zope.traversing.browser import absoluteURL
        url = absoluteURL(self.context, self.request)
        return '%s/thankyou.html?id=%s' % (url, self.clientName)
