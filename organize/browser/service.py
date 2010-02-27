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

    def getFromTo(self, service=None):
        if service is None:
            service = self.context
        if service.start and service.end:
            typeEnd = 'time'
            separator = '-'
            if self.isMultiDay(service):
                typeEnd = 'dateTime'
                separator = ' - '
            return ('%s%s%s' %
                (self.getFormattedDate(service.start,
                                       type='dateTime', variant='short'),
                 separator,
                 self.getFormattedDate(service.end, type=typeEnd, variant='short')))
        else:
            return '-'

    def getFromToDate(self, service=None):
        if service is None:
            service = self.context
        end = ''
        if service.start and service.end:
            start = self.getFormattedDate(service.start, type='date', variant='short')
            end = ''
            if self.isMultiDay(service):
                end = ' - ' + self.getFormattedDate(service.end, type='date',
                                                    variant='short')
            return start + end
        else:
            return '-'

    def getFromToTime(self, service=None):
        if service is None:
            service = self.context
        if service.start and service.end:
            start = self.getFormattedDate(service.start, type='time', variant='short')
            end = self.getFormattedDate(service.end, type='time', variant='short')
            return '%s - %s' % (start, end)
        else:
            return '-'

    def isMultiDay(self, service):
        return time.localtime(service.start)[2] != time.localtime(service.end)[2]

    def getCost(self, service=None):
        if service is None:
            service = self.context
        #value = service.getCost()
        value = service.cost
        if value:
            return ('%.2f Euro' % float(value)).replace('.', ',')
        return u''


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

    def overview(self, includeCategories=None, skipInactive=False):
        result = []
        classific = []
        category = None
        svcs = sorted((svc.getCategory(), idx, svc)
                for idx, svc in enumerate(self.context.getServices()))
        for cat, idx, svc in svcs:
            if includeCategories and cat not in includeCategories:
                continue
            if skipInactive and not svc.isActive():
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
        #clientRegs = IClientRegistrations(client)
        #regs = sorted(clientRegs.getRegistrations(), key=self.sortKey)
        regs = self.registrationsInfo
        instance = IInstance(client)
        data = instance.applyTemplate()
        data['service_registrations'] = regs
        data['info_messages'] = [item['info'] for item in regs if item['info']]
        data['errors'] = [item['error'] for item in regs if item['error']]
        return data

    def sortKey(self, reg):
        return reg.service.start

    def update(self):
        client = self.getClient()
        if client is None:
            return True     # TODO: error, redirect to overview
        data = self.getClientData()
        if data.get('errors'):
            return True
        form = self.request.form
        #clientName = self.getClientName()
        if not form.get('action'):
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
        clientRegs = IClientRegistrations(client)
        regs = sorted(clientRegs.getRegistrations(), key=self.sortKey)
        for reg in regs:
            info = error = u''
            service = reg.service
            if (service.capacity >= 0 and
                    IStateful(reg).state == 'temporary' and
                    service.getNumberRegistered() + reg.number > service.capacity):
                service.unregister(client)
                clientRegs.unregister([service])
                info = error = u'capacity_exceeded'
            result.append(dict(service=service.title or '???',
                               waitingList=service.waitingList,
                               fromTo=self.getFromTo(service),
                               fromToDate=self.getFromToDate(service),
                               fromToTime=self.getFromToTime(service),
                               isMultiDay=self.isMultiDay(service),
                               location=service.location or '',
                               locationUrl=service.locationUrl or '',
                               number=reg.number,
                               numberWaiting=reg.numberWaiting,
                               externalId=service.externalId or '',
                               cost=self.getCost(service),
                               info=info,
                               error=error,
                               serviceObject=service))
        return result

    @Lazy
    def registrationsInfo(self):
        return self.getRegistrationsInfo()

    @Lazy
    def hasWaiting(self):
        for reg in self.registrationsInfo:
            if reg['numberWaiting'] > 0:
                return True
        return False

    @Lazy
    def hasCost(self):
        for reg in self.registrationsInfo:
            if reg['cost']:
                return True
        return False

    @Lazy
    def hasExternalId(self):
        for reg in self.registrationsInfo:
            if reg['externalId']:
                return True
        return False

    def getLocationInfo(self, info):
        location, locationUrl = info['location'], info['locationUrl']
        if locationUrl and locationUrl.startswith('/'):
            locationUrl = self.request.get('SERVER_URL') + locationUrl
        locationInfo = (locationUrl and '%s (%s)' % (location, locationUrl)
                                    or location)
        return locationInfo

    def listRegistrationsTextTable(self):
        result = []
        for info in self.registrationsInfo:
            line = '%-30s %27s' % (info['service'], info['fromTo'])
            if info['serviceObject'].allowRegWithNumber:
                line += ' %4i' % info['number']
            result.append(line)
        return '\n'.join(result)

    def listRegistrationsText(self):
        result = []
        for info in self.registrationsInfo:
            lineData = []
            if not info['number'] and not info['numberWaiting']:
                continue
            locationInfo = self.getLocationInfo(info)
            lineData = [info['service'],
                        'Datum: ' + info['fromToDate'],
                        'Uhrzeit: ' + info['fromToTime'],
                        locationInfo]
            if info['cost']:
                lineData.append('Kostenbeitrag: %s' % info['cost'])
            if info['externalId']:
                lineData.append('Code: %s' % info['externalId'])
            if info['serviceObject'].allowRegWithNumber and info['number']:
                lineData.append('Teilnehmer: %s' % info['number'])
            if info['numberWaiting']:
                waitingInfo = 'Teilnehmer auf Warteliste'
                if info['serviceObject'].allowRegWithNumber:
                    waitingInfo += ': %s' % info['numberWaiting']
                lineData.append(waitingInfo)
            lineData.append('')
            line = '\n'.join(lineData)
            result.append(line)
        return '\n'.join(result)

    def listRegistrationsWaitingText(self):
        result = []
        for info in self.registrationsInfo:
            if not info['numberWaiting']:
                continue
            locationInfo = self.getLocationInfo(info)
            line = '\n'.join((info['service'], info['fromTo'], locationInfo))
            if info['serviceObject'].allowRegWithNumber:
                line += '\nTeilnehmer: %s\n' % info['numberWaiting']
            result.append(line)
        return '\n'.join(result)

    html = '''
        <table class="listing" style="width: 100%%">
          <tr>
            <th width="5%%">Teilnehmer</th>%s
            <th>Angebot</th>
            <th>Datum/Uhrzeit</th>
            <th>Ort</th>
            %s %s
          </tr>
          %s
        </table>
    '''
    row = '''
          <tr>
            <td width="5%%">%i</td>%s
            <td>%s</td>
            <td style="white-space: nowrap">%s</td>
            <td>%s</td>
            %s %s
          </tr>
    '''
    def listRegistrationsHtml(self):
        result = []
        waitingHeader = costHeader = externalIdHeader = ''
        waitingRow = '<td width="5%%">%i</td>'
        costRow = '<td>%s</td>'
        externalIdRow = '<td>%s</td>'
        if self.hasWaiting:
            waitingHeader = '<th width="5%%">Warteliste</th>'
        if self.hasCost:
            costHeader = '<th>Kostenbeitrag</th>'
        if self.hasExternalId:
            externalIdHeader = '<th style="white-space: nowrap">Code</th>'
        for info in self.getRegistrationsInfo():
            location, locationUrl = info['location'], info['locationUrl']
            locationInfo = (locationUrl
                        and ('<a href="%s">%s</a>'  % (locationUrl, location))
                        or location)
            line = self.row % (info['number'],
                            self.hasWaiting and
                                    waitingRow % info['numberWaiting'] or '',
                            info['service'],
                            info['fromToDate'] + '<br />' + info['fromToTime'],
                            locationInfo,
                            self.hasCost and
                                    costRow % info['cost'] or '',
                            self.hasExternalId and
                                    externalIdRow % info['externalId'] or '',
                            )
            result.append(line)
        return self.html % (waitingHeader, costHeader, externalIdHeader,
                            '\n'.join(result))


class ServiceView(BaseView):

    showCheckoutButton = False
    state = None

    def getRegistrations(self):
        return self.context.registrations

    def listRegistrations(self):
        if self.request.get('with_temporary'):
            return self.getRegistrations()
        regs = self.getRegistrations()
        return (name for name, reg in regs.items()
                  if IStateful(reg).getState() != 'temporary')

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
        if not context.isActive():
            return False
        if not context.allowDirectRegistration:
            return False
        return (self.capacityAvailable() or self.context.waitingList
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
        return dict(number=registration.number,
                    numberWaiting=registration.numberWaiting,
                    state=state.name, stateTitle=state.title)

    @Lazy
    def registeredTotalSubmitted(self):
        # TODO: clean-up temporary registrations
        # return self.context.getNumberRegistered()
        total = 0
        for reg in self.getRegistrations().values():
            state = IStateful(reg).getStateObject()
            if state.name != 'temporary':
                total += reg.number
        return total

    @Lazy
    def registeredTotalsSubmitted(self):
        # TODO: clean-up temporary registrations
        # return self.context.getNumberRegistered()
        total = totalWaiting = 0
        for reg in self.getRegistrations().values():
            state = IStateful(reg).getStateObject()
            if state.name != 'temporary':
                total += reg.number
                totalWaiting += reg.numberWaiting
        if not self.context.waitingList:
            totalWaiting = ''
        return dict(number=total, numberWaiting=totalWaiting)

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
        if not service.isActive():
            return False
        return (self.capacityAvailable(service) or service.waitingList
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
        client = None
        form = self.request.form
        clientName = self.getClientName()
        if not form.get('action'):
            return True
        manager = self.context.getManager()
        if clientName:
            client = manager.getClients().get(clientName)
            #if client is None:
            #    return True
        if client is None:
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
