#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
from cybertools.composer.rule.base import Event
from cybertools.composer.rule.interfaces import IRuleManager
from cybertools.composer.schema.browser.common import BaseView
from cybertools.composer.schema.client import eventTypes, getCheckoutRule
from cybertools.composer.schema.interfaces import IClientFactory, ISchema
from cybertools.composer.schema.schema import FormState
from cybertools.stateful.interfaces import IStateful
from cybertools.util.jeep import Jeep


class SchemaView(BaseView):
    """ View for schema objects.
    """

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
            self.request.response.redirect(self.getNextUrl())
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
        ignoreValidation = (self.getButtonAction() == 'submit_previous')
        self.formState = formState = instance.applyTemplate(form,
                                            ignoreValidation=ignoreValidation)
        if formState.severity > 0 and not ignoreValidation:
            # show form again; do not add client to manager
            return True
        if newClient:
            clientName = manager.addClient(client)
            self.setClientName(clientName)
        self.request.response.redirect(self.getNextUrl())
        return False


class FormManagerView(BaseView):

    isManageMode = False

    @Lazy
    def manager(self):
        return self.context

    def update(self):
        if self.isManageMode:
            return True
        self.context.request.response.redirect(self.firstFormUrl())
        #for tpl in self.context.getClientSchemas():
        #    self.context.request.response.redirect(absoluteURL(tpl, self.request))
        #    break
        return False

    def overview(self, ignoreTemporary=True):
        result = []
        for c in self.context.getClients().values():
            state = IStateful(c).state
            if ignoreTemporary and state == 'temporary':
                continue
            instance = IInstance(c)
            data = instance.applyTemplate()
            data['id'] = data['__name__']
            data['state'] = state
            result.append(data)
        return result

    def firstFormUrl(self):
        for tpl in self.context.getClientSchemas():
            return absoluteURL(tpl, self.request)


class CheckoutView(BaseView):

    def getClient(self):
        clientName = self.getClientName()
        if clientName is None:
            return None
        return self.context.getClients().get(clientName)

    def getClientData(self):
        client = self.getClient()
        if client is None:
            return {}
        instance = IInstance(client)
        data = instance.applyTemplate()
        return data

    def update(self):
        data = self.getClientData()
        if data.get('errors'):
            return True
        form = self.request.form
        #clientName = self.getClientName()
        if not form.get('action'):
            return True     # TODO: error, redirect to overview
        client = self.getClient()
        if client is None:
            return True     # TODO: error, redirect to overview
        # submit
        stf = IStateful(client)
        if stf.state == 'temporary':
            stf.doTransition('submit')
        # send mail
        rm = IRuleManager(self.context)
        rm.addRule(getCheckoutRule(self.context.senderEmail))
        result = rm.handleEvent(Event(eventTypes['client.checkout'],
                                      client, self.request))
        #params = '?message=thankyou&id=' + self.clientName
        #self.request.response.redirect(self.url + '/checkout.html' + params)
        return False
