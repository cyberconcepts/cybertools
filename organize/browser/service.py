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
from cybertools.composer.schema.browser.common import BaseView as SchemaBaseView
from cybertools.composer.schema.interfaces import IClientFactory
from cybertools.util.format import formatDate


class BaseView(object):

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

    def findRegistrationTemplate(self, service):
        """ Find a registration template that provides the registration
            for the service given.
        """
        for tpl in self.context.getClientSchemas():
            if IRegistrationTemplate.providedBy(tpl):
                # TODO: check that service is really provided by this template
                return tpl
        return None

    def overview(self):
        result = []
        classific = []
        category = None
        maxLevel = 0
        svcs = sorted(self.context.getServices(),
                      key=lambda x: (x.getCategory(),
                                     x.getClassification(),
                                     x.title))
        for svc in svcs:
            cat = svc.getCategory()
            if cat != category:
                term = serviceCategories.getTermByToken(cat)
                result.append(dict(isHeadline=True, level=0, title=term.title,
                                   object=None))
                category = cat
                classific = []
            clsf = svc.getClassification()
            for idx, element in enumerate(clsf):
                level = idx + 1
                if (len(classific) <= idx or
                        classific[idx].name != element.name):
                    result.append(dict(isHeadline=True, level=level,
                                       title=element.title,
                                       object=element.object))
                    classific = clsf
                if level > maxLevel:
                    maxLevel = level
            result.append(dict(isHeadline=False, level=maxLevel+1,
                               title=svc.title or svc.getName(),
                               fromTo=self.getFromTo(svc),
                               object=svc))
        return result


class ServiceView(BaseView):

    def getRegistrations(self):
        return self.context.registrations

    def registrationUrl(self):
        context = self.context
        man = context.getManager()
        tpl = ServiceManagerView(man, self.request).findRegistrationTemplate(context)
        return self.getUrlForObject(tpl)


class RegistrationTemplateView(SchemaBaseView):

    @Lazy
    def services(self):
        return self.getServices()

    def getServices(self):
        return self.context.getServices().values()

    def getRegistrations(self):
        if not self.clientName:
            form = self.request.form
            self.clientName = form.get('id')
        clientName = self.clientName
        if not clientName:
            return []
        manager = self.context.getManager()
        client = manager.getClients().get(clientName)
        if client is None:
            return []
        regs = IClientRegistrations(client)
        regs.template = self.context
        return regs.getRegistrations()

    def getRegistratedServicesTokens(self):
        return [r.service.token for r in self.getRegistrations()]

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
        regs = IClientRegistrations(client)
        regs.template = self.context
        allServices = self.getServices()
        oldServices = [r.service for r in regs.getRegistrations()]
        newServices = [manager.getServices()[token]
                       for token in form.get('service_tokens', [])]
        regs.register(newServices)
        toDelete = [s for s in oldServices
                      if s in allServices and s not in newServices]
        regs.unregister(toDelete)
        #return True
        self.request.response.redirect(self.nextUrl())
        return False
