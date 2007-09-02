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

from datetime import datetime
import time
from zope import component
from zope.cachedescriptors.property import Lazy

from cybertools.organize.interfaces import IClientRegistrations, IRegistrationTemplate
from cybertools.organize.interfaces import serviceCategories
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.browser.common import BaseView as SchemaBaseView
from cybertools.composer.schema.interfaces import IClientFactory
from cybertools.util.format import formatDate


class BaseView(SchemaBaseView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def url(self):
        return self.getUrlForObject(self.context)

    def getUrlForObject(self, obj):
        from zope.traversing.browser import absoluteURL
        return absoluteURL(obj, self.request)

    def getLanguage(self):
        # TODO: take from request or whatever...
        return 'en'

    def getFormattedDate(self, date=None, type='date', variant='medium'):
        date = time.localtime(date)[:6]
        date = datetime(*date)
        return formatDate(date, type=type, variant=variant, lang=self.getLanguage())

    def getFromTo(self, service=None):
        if service is None:
            service = self.context
        if service.start and service.end:
            return ('%s - %s' %
                (self.getFormattedDate(service.start, type='dateTime', variant='short'),
                 self.getFormattedDate(service.end, type='time', variant='short')))
        else:
            return '-'


class ServiceManagerView(BaseView):

    def getCustomView(self):
        viewName = self.context.getViewName()
        if viewName:
            return component.getMultiAdapter((self.context, self.request),
                                             name=viewName)
        return None

    def findRegistrationTemplate(self, service):
        """ Find a registration template that provides the registration
            for the service given.
        """
        for tpl in self.context.getClientSchemas():
            if IRegistrationTemplate.providedBy(tpl):
                # TODO: check that service is really provided by this template
                return tpl
        return None

    def overview(self, includeCategories=None):
        result = []
        classific = []
        category = None
        maxLevel = 0
        svcs = sorted((svc.getCategory(), idx, svc)
                for idx, svc in enumerate(self.context.getServices()))
        for cat, idx, svc in svcs:
            if includeCategories and cat not in includeCategories:
                continue
            if cat != category:
                term = serviceCategories.getTermByToken(cat)
                result.append(dict(isHeadline=True, level=0, title=term.title,
                                   name=cat,
                                   object=None))
                category = cat
                classific = []
            clsf = svc.getClassification()
            for idx, element in enumerate(clsf):
                level = idx + 1
                if (len(classific) <= idx or
                        classific[idx].name != element.name):
                    result.append(dict(isHeadline=True, level=level,
                                       name=element.name,
                                       title=element.title,
                                       object=element.object))
                    classific = clsf
                if level > maxLevel:
                    maxLevel = level
            result.append(dict(isHeadline=False, level=maxLevel+1,
                               name=svc.getName(),
                               title=svc.title or svc.getName(),
                               fromTo=self.getFromTo(svc),
                               object=svc))
        return result

    def eventsOverview(self):
        return self.overview(includeCategories=('event',))


class ServiceView(BaseView):

    showCheckoutButton = False

    def getRegistrations(self):
        return self.context.registrations

    def getRegistrationTemplate(self):
        context = self.context
        man = context.getManager()
        return ServiceManagerView(man, self.request).findRegistrationTemplate(context)

    def registrationUrl(self):
        tpl = self.getRegistrationTemplate()
        return self.getUrlForObject(tpl)

    def getClientData(self):
        clientName = self.getClientName()
        if clientName is None:
            return {}
        data = self.getDataForClient(clientName)
        regs = self.getRegistrations()
        reg = regs.get(clientName)
        if reg:
            data['service_registration'] = reg
        return data

    def getDataForClient(self, clientName):
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return {}
        instance = IInstance(client)
        return instance.applyTemplate()

    def update(self):
        newClient = False
        nextUrl = None
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            data = self.getClientData()
            if ('service_registration' in data
                    and data['service_registration'].number > 0):
                self.showCheckoutButton = True
            return True
        manager = self.context.getManager()
        if clientName:
            client = manager.getClients().get(clientName)
            if client is None:
                return True
        else:
            client = IClientFactory(manager)()
            clientName = manager.addClient(client)
            self.setClientName(clientName)
            newClient = True
            nextUrl = self.getSchemaUrl()
        regs = IClientRegistrations(client)
        try:
            number = int(form.get('number', 1))
        except ValueError:
            number = 1
        if 'submit_register' in form and number > 0:
            regs.register([self.context], numbers=[number])
            self.showCheckoutButton = True
        elif 'submit_unregister' in form:
            regs.unregister([self.context])
            number = 0
        elif 'submit_checkout' in form:
            nextUrl = self.getSchemaUrl()
        if nextUrl:
            self.request.response.redirect(nextUrl)
            return False
        return True

    def getSchemaUrl(self):
        manager = self.context.getManager()
        return self.getUrlForObject(manager.getClientSchemas()[0])


class RegistrationTemplateView(BaseView):

    @Lazy
    def services(self):
        return self.getServices()

    def getServices(self):
        return self.context.getServices().values()

    def getRegistrations(self):
        clientName = self.getClientName()
        if not clientName:
            return []
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return []
        regs = IClientRegistrations(client)
        regs.template = self.context
        return regs.getRegistrations()

    def getRegisteredServicesTokens(self):
        return [r.service.token for r in self.getRegistrations()]

    def getRegistrationsDict(self):
        return dict((r.service.token, r) for r in self.getRegistrations())

    def getData(self):
        """ Retrieve standard field data (accessible without providing
            a template) from the client object.
        """
        clientName = self.getClientName()
        if not clientName:
            return {}
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return {}
        instance = IInstance(client)
        return instance.applyTemplate()

    def update(self):
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            return True
        manager = self.context.getManager()
        if clientName:
            client = manager.getClients().get(clientName)
            if client is None:
                return True
        else:
            client = IClientFactory(manager)()
            clientName = manager.addClient(client)
            self.setClientName(clientName)
        regs = IClientRegistrations(client)
        regs.template = self.context
        services = manager.getServices()  # a mapping!
        allServices = services.values()
        oldServices = [r.service for r in regs.getRegistrations()]
        # collect check boxes:
        newServices = [services[token]
                       for token in form.get('service_tokens', [])]
        # collect numerical input:
        numbers = len(newServices) * [1]
        for token, svc in services.items():
            try:
                value = int(form.get('service.' + token, 0))
            except ValueError:
                value = 1
            if value > 0:
                newServices.append(svc)
                numbers.append(value)
        regs.register(newServices, numbers=numbers)
        toDelete = [s for s in oldServices
                      if s in allServices and s not in newServices]
        regs.unregister(toDelete)
        #return True
        self.request.response.redirect(self.nextUrl())
        return False
