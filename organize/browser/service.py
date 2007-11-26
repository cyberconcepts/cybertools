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
from cybertools.organize.service import eventTypes, getCheckoutRule
from cybertools.composer.interfaces import IInstance
from cybertools.composer.rule.base import Event
from cybertools.composer.rule.interfaces import IRuleManager
from cybertools.composer.schema.browser.common import BaseView as SchemaBaseView
from cybertools.composer.schema.interfaces import IClientFactory
from cybertools.stateful.interfaces import IStateful
from cybertools.util.format import formatDate


class BaseView(SchemaBaseView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def url(self):
        return self.getUrlForObject(self.context)

    def getClient(self):
        clientName = self.getClientName()
        if clientName is None:
            return None
        return self.manager.getClients().get(clientName)

    # output formatting

    def getFormattedDate(self, date=None, type='date', variant='medium'):
        date = time.localtime(date)[:6]
        date = datetime(*date)
        return formatDate(date, type=type, variant=variant, lang=self.getLanguage())

    def getFromTo(self, service=None):
        if service is None:
            service = self.context
        if service.start and service.end:
            return ('%s-%s' %
                (self.getFormattedDate(service.start,
                        type='dateTime', variant='short').replace(' ', '  '),
                 self.getFormattedDate(service.end, type='time', variant='short')))
        else:
            return '-'


class ServiceManagerView(BaseView):

    isManageMode = False

    def getCustomView(self):
        if self.isManageMode:
            return None
        viewName = self.context.getViewName()
        if viewName:
            return component.getMultiAdapter((self.context, self.request),
                                             name=viewName)
        return None

    @Lazy
    def manager(self):
        return self.context

    def getRegistrationTemplate(self, service=None, preferRegistrationTemplate=False):
        """ Find a suitable data or registration template.
        """
        first = None
        for tpl in self.context.getClientSchemas():
            if not preferRegistrationTemplate:
                return tpl
            if IRegistrationTemplate.providedBy(tpl):
                # TODO (optional): make sure template provides registration
                # for service given.
                return tpl
            if first is None:
                first = tpl
        return first

    #@Lazy - Zope 2.9 compatibility
    def registrationUrl(self):
        tpl = self.getRegistrationTemplate()
        return self.getUrlForObject(tpl)

    def redirectToRegistration(self):
        self.request.response.redirect(self.registrationUrl())
        return 'redirect'  # let template skip rendering

    def overview(self, includeCategories=None):
        result = []
        classific = []
        category = None
        svcs = sorted((svc.getCategory(), idx, svc)
                for idx, svc in enumerate(self.context.getServices()))
        for cat, idx, svc in svcs:
            if includeCategories and cat not in includeCategories:
                continue
            level = 0
            if cat != category:
                term = serviceCategories.getTermByToken(cat)
                result.append(dict(isHeadline=True, level=level, title=term.title,
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
                                       object=element.object,
                                       view=None))
                    classific = clsf[:idx+1]
            result.append(dict(isHeadline=False, level=level+1,
                               name=svc.getName(),
                               title=svc.title or svc.getName(),
                               fromTo=self.getFromTo(svc),
                               object=svc,
                               view=ServiceView(svc, self.request)))
        return result

    def eventsOverview(self):
        return self.overview(includeCategories=('event',))


class CheckoutView(ServiceManagerView):

    def getServices(self):
        return self.manager.getServices()

    def getClientData(self):
        client = self.getClient()
        if client is None:
            return {}
        regs = IClientRegistrations(client)
        instance = IInstance(client)
        data = instance.applyTemplate()
        data['service_registrations'] = sorted(regs.getRegistrations(),
                                               key=self.sortKey)
        return data

    def sortKey(self, reg):
        return reg.service.start

    def update(self):
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            return True     # TODO: error, redirect to overview
        client = self.getClient()
        if client is None:
            return True     # TODO: error, redirect to overview
        regs = IClientRegistrations(client).getRegistrations()
        for reg in regs:
            stateful = IStateful(reg)
            stateful.doTransition(('submit', 'change'))
        # send mail
        rm = IRuleManager(self.manager)
        rm.addRule(getCheckoutRule(self.manager.senderEmail))
        result = rm.handleEvent(Event(eventTypes['service.checkout'],
                                      client, self.request))
        #params = '?message=thankyou&id=' + self.clientName
        #self.request.response.redirect(self.url + '/checkout.html' + params)
        return False

    def getRegistrationsInfo(self):
        client = self.getClient()
        if client is None:
            return []
        result = []
        regs = IClientRegistrations(client)
        regs = sorted(regs.getRegistrations(), key=self.sortKey)
        for reg in regs:
            service = reg.service
            result.append(dict(service=service.title,
                               fromTo=self.getFromTo(service),
                               location=service.location,
                               number=reg.number,
                               serviceObject=service))
        return result

    def listRegistrationsTextTable(self):
        result = []
        for info in self.getRegistrationsInfo():
            line = '%-30s %27s' % (info['service'], info['fromTo'])
            if info['serviceObject'].allowRegWithNumber:
                line += ' %4i' % info['number']
            result.append(line)
        return '\n'.join(result)

    def listRegistrationsText(self):
        result = []
        for info in self.getRegistrationsInfo():
            line = '\n'.join((info['service'], info['fromTo'], info['location']))
            if info['serviceObject'].allowRegWithNumber:
                line += '\nTeilnehmer: %s\n' % info['number']
            result.append(line)
        return '\n'.join(result)

    html = '''
        <table class="listing" style="width: 100%%">
          <tr>
            <th width="5%%">Teilnehmer</th>
            <th>Angebot</th>
            <th>Datum/Uhrzeit</th>
            <th>Ort</th>
          </tr>
          %s
        </table>
    '''
    row = '''
          <tr>
            <td width="5%%">%i</td>
            <td>%s</td>
            <td style="white-space: nowrap">%s</td>
            <td>%s</td>
          </tr>
    '''
    def listRegistrationsHtml(self):
        result = []
        for info in self.getRegistrationsInfo():
            line = self.row % (info['number'], info['service'],
                        info['fromTo'].replace(' ', '&nbsp;&nbsp;'),
                        info['location'])
            result.append(line)
        return self.html % '\n'.join(result)


class ServiceView(BaseView):

    showCheckoutButton = False
    state = None

    def getRegistrations(self):
        return self.context.registrations

    def getRegistrationTemplate(self):
        context = self.context
        man = context.getManager()
        return ServiceManagerView(man, self.request).getRegistrationTemplate()

    #@Lazy - Zope 2.9 compatibility
    def registrationUrl(self):
        tpl = self.getRegistrationTemplate()
        return self.getUrlForObject(tpl)

    def allowRegistration(self):
        context = self.context
        if not context.allowDirectRegistration:
            return False
        return (self.capacityAvailable()
                or self.getClientName() in context.registrations)

    def capacityAvailable(self):
        return not self.context.capacity or self.context.availableCapacity

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

    def getRegistrationInfo(self, reg):
        registration = self.getRegistrations()[reg]
        state = IStateful(registration).getStateObject()
        number=registration.number
        return dict(number=number, state=state.name, stateTitle=state.title)

    @Lazy
    def registeredTotalSubmitted(self):
        total = 0
        for reg in self.getRegistrations().values():
            state = IStateful(reg).getStateObject()
            if state.name != 'temporary':
                total += reg.number
        return total

    def update(self):
        newClient = False
        nextUrl = None
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            #data = self.getClientData()
            #if ('service_registration' in data
            #        and data['service_registration'].number > 0):
            #    self.showCheckoutButton = True
            return True
        manager = self.context.getManager()
        try:
            number = int(form.get('number', 0))
            if number < 0:
                number = 0
        except ValueError:
            number = 0
        if clientName:
            client = manager.getClients().get(clientName)
            if client is None:
                self.request.response.redirect(self.getSchemaUrl())
                return False
        else:
            if number == 0:
                self.request.response.redirect(self.getSchemaUrl())
                return False
            else:
                client = IClientFactory(manager)()
                newClient = True
                nextUrl = self.getSchemaUrl()
        regs = self.state = IClientRegistrations(client)
        regs.validate(clientName, [self.context], [number])
        if regs.severity > 0:
            return True
        if newClient:
            clientName = manager.addClient(client)
            self.setClientName(clientName)
        if 'submit_register' in form and number > 0:
            regs.register([self.context], numbers=[number])
            self.showCheckoutButton = True
            nextUrl = self.getSchemaUrl()
        elif 'submit_register' in form and number == 0 or 'submit_unregister' in form:
            regs.unregister([self.context])
            number = 0
            nextUrl = self.getSchemaUrl()
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

    state = None

    @Lazy
    def services(self):
        return self.getServices()

    def getServices(self):
        return self.context.getServices()
        #return sorted(self.context.getServices().values(), key=self.sortKey)

    def overview(self):
        categories = self.context.categories or None
        mv = ServiceManagerView(self.context.getManager(), self.request)
        return mv.overview(categories)

    def sortKey(self, svc):
        return (svc.category, svc.getClassification(), svc.start)

    def allowRegistration(self, service):
        return (self.capacityAvailable(service)
                or service in self.getRegisteredServices())

    def capacityAvailable(self, service):
        return not service.capacity or service.availableCapacity

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

    def getRegisteredServices(self):
        return [r.service for r in self.getRegistrations()]

    def getRegisteredServicesTokens(self):
        return [s.token for s in self.getRegisteredServices()]

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
        newClient = False
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
            newClient = True    # make persistent later
        regs = self.state = IClientRegistrations(client)
        regs.template = self.context
        services = manager.getServices()  # a mapping!
        allServices = services.values()
        # collect check boxes:
        newServices = [services[token]
                       for token in form.get('service_tokens', [])]
        # collect numerical input:
        numbers = len(newServices) * [1]
        for token, svc in services.items():
            try:
                value = int(form.get('service.' + token, 0))
            except ValueError:
                value = 0
            if value > 0:
                newServices.append(svc)
                numbers.append(value)
        regs.validate(clientName, newServices, numbers)
        if regs.severity > 0:
            return True
        if newClient:
            clientName = manager.addClient(client)
            self.setClientName(clientName)
        regs.register(newServices, numbers=numbers)
        oldServices = [r.service for r in regs.getRegistrations()]
        toDelete = [s for s in oldServices
                      if s in allServices and s not in newServices]
        regs.unregister(toDelete)
        self.request.response.redirect(self.getNextUrl())
        return False


