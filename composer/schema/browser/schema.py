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

from cybertools.composer.schema.browser.common import BaseView
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.interfaces import IClientFactory
from cybertools.composer.schema.schema import FormState


class SchemaView(BaseView):

    formState = FormState()

    isManageMode = False

    @Lazy
    def fields(self):
        return self.context.fields

    @Lazy
    def data(self):
        return self.getData()

    def getData(self):
        form = self.request.form
        clientName = self.getClientName()
        if not clientName:
            return {}
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return {}
        instance = IInstance(client)
        instance.template = self.context
        data = instance.applyTemplate(mode='edit')
        for k, v in data.items():
            #overwrite data with values from form
            if k in form:
                data[k] = form[k]
        return data

    def update(self):
        newClient = False
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            return True
        if self.isManageMode:
            # Don't store anything when editing
            self.request.response.redirect(self.nextUrl())
            return False
        manager = self.context.getManager()
        if clientName:
            client = manager.getClients().get(clientName)
            if client is None:
                # no valid clientName - show empty form
                return True
            #self.setClientName(clientName) # store in view and session
        else:
            client = IClientFactory(manager)()
            # only add client to manager after validation, so we have
            # to keep the info about new client here
            newClient = True
        instance = component.getAdapter(client, IInstance, name='editor')
        instance.template = self.context
        self.formState = formState = instance.applyTemplate(form)
        if formState.severity > 0:
            # show form again; do not add client to manager
            return True
        if newClient:
            clientName = manager.addClient(client)
            self.setClientName(clientName)
        self.request.response.redirect(self.nextUrl())
        return False

