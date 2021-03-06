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
Service management classes.

$Id$
"""

from time import time
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope import component
from zope.interface import implements, Interface

from cybertools.composer.interfaces import IInstance
from cybertools.composer.message.base import MessageManager
from cybertools.composer.rule.base import RuleManager, EventType
from cybertools.composer.rule.base import Rule, Action
from cybertools.composer.schema.interfaces import IClientManager, IClient
from cybertools.composer.schema.client import ClientManager
from cybertools.stateful.base import StatefulAdapter
from cybertools.stateful.definition import registerStatesDefinition
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStateful
from cybertools.util.jeep import Jeep
from cybertools.util.randomname import generateName
from cybertools.organize.interfaces import IServiceManager
from cybertools.organize.interfaces import IService, IScheduledService
from cybertools.organize.interfaces import IServiceCollection
from cybertools.organize.interfaces import IRegistration, IRegistrationTemplate
from cybertools.organize.interfaces import IClientRegistrations


class ServiceManager(ClientManager):

    implements(IServiceManager)

    servicesFactory = Jeep
    services = None

    allowRegWithNumber = False
    allowDirectRegistration = True

    def __init__(self):
        if self.servicesFactory is not None:
            self.services = self.servicesFactory()
        super(ServiceManager, self).__init__()

    def getServices(self, categories=[]):
        return self.services


class Registration(object):

    implements(IRegistration)

    number = 1
    numberWaiting = 0

    def __init__(self, client, service, number=1, numberWaiting=0):
        self.client = client
        self.service = service
        self.timeStamp = int(time())
        self.number = number
        self.numberWaiting = numberWaiting


class PersistentRegistration(Registration, Persistent):

    pass


class Service(object):

    implements(IService)

    registrationsFactory = OOBTree
    registrationFactory = PersistentRegistration
    subservicesFactory = Jeep
    collectionsFactory = set

    manager = None
    parent = None
    subservices = None
    collections = None

    bookable = True
    category = None
    location = locationUrl = externalId = u''
    cost = 0.0
    allowRegWithNumber = False
    allowDirectRegistration = True
    waitingList = False
    presetRegistrationField = False

    def __init__(self, name=None, title=u'', capacity=-1, **kw):
        self.name = self.__name__ = name
        self.title = title
        self.capacity = capacity
        if self.registrationsFactory is not None:
            self.registrations = self.registrationsFactory()
        if self.subservicesFactory is not None:
            self.subservices = self.subservicesFactory()
        if self.collectionsFactory is not None:
            self.collections = self.collectionsFactory()
        self.classification = []
        for k, v in kw.items():
            setattr(self, k, v)

    def getName(self):
        return self.name

    def getManager(self):
        return self.manager

    def getSubservices(self):
        return self.subservices.values()

    def addSubservice(self, service):
        self.subservices.append(service)

    def removeSubservice(self, service):
        del self.subservices[service.name]

    def getParentService(self):
        return self.parent

    def getServiceCollections(self):
        return self.collections.values()

    def getClassification(self):
        return self.classification

    def getCategory(self):
        return self.category

    @property
    def token(self):
        return self.getToken()

    def getToken(self):
        return self.name

    def isActive(self):
        return True

    def getAvailableCapacity(self, ignoreWaiting=False):
        if not ignoreWaiting and self.getNumberWaiting() > 0:
            return 0
        number = self.getNumberRegistered()
        if self.capacity >= 0 and number >= self.capacity:
            return 0
        return self.capacity - number

    @property
    def availableCapacity(self):
        return self.getAvailableCapacity()

    def register(self, client, number=1):
        clientName = client.__name__
        numberWaiting = current = currentWaiting = 0
        reg = None
        if clientName in self.registrations:
            reg = self.registrations[clientName]
            current = reg.number
            currentWaiting = reg.numberWaiting
        if currentWaiting and self.waitingList:
            numberWaiting = number - current - self.getAvailableCapacity(True)
            number = number - numberWaiting
        elif (self.waitingList and self.availableCapacity >= 0
                    and number > (self.availableCapacity + current)):
            numberWaiting = number - current - self.availableCapacity
            #number = self.availableCapacity + current
            number = number - numberWaiting
        if reg is not None:
            if number != reg.number:
                reg.number = number
                # TODO: set timeStamp
            if numberWaiting != reg.numberWaiting:
                reg.numberWaiting = numberWaiting
            return reg
        reg = self.registrationFactory(client, self, number, numberWaiting)
        self.registrations[clientName] = reg
        return reg

    def unregister(self, client):
        clientName = client.__name__
        if clientName in self.registrations:
            reg = self.registrations[clientName]
            reg.number = reg.numberWaiting = 0
            del self.registrations[clientName]

    def getNumberRegistered(self, ignoreTemporary=True):
        result = 0
        for r in self.registrations.values():
            if ignoreTemporary and IStateful(r).state == 'temporary':
                continue
            result += r.number
        return result

    def getNumberWaiting(self, ignoreTemporary=True):
        if not self.waitingList:
            return 0
        result = 0
        for r in self.registrations.values():
            if ignoreTemporary and IStateful(r).state == 'temporary':
                continue
            result += r.numberWaiting
        return result

    # default methods
    def getAllowRegWithNumberFromManager(self):
        return getattr(self.getManager(), 'allowRegWithNumber', None)
    def getAllowDirectRegistrationFromManager(self):
        return getattr(self.getManager(), 'allowDirectRegistration', None)


class ScheduledService(Service):

    implements(IScheduledService)

    start = end = None

    # default methods
    def getStartFromManager(self):
        return getattr(self.getManager(), 'start', None)
    def getEndFromManager(self):
        return getattr(self.getManager(), 'end', None)


class ServiceCollection(ScheduledService):

    implements(IServiceCollection)

    assignmentsFactory = set

    assignments = None
    collectionType = u'day'

    def __init__(self, name=None, title=u'', capacity=-1, **kw):
        super(ServiceCollection, self).__init__(name, title, capacity, kw)
        if self.assignmentsFactory is not None:
            self.assignments = self.assignmentsFactory()

    def getAssignedServices(self):
        return self.assignments

    def assignService(self, service):
        self.assignments.add(service)

    def deassignService(self, service):
        self.assignments.remove(service)


# registration stuff

class RegistrationTemplate(object):

    implements(IRegistrationTemplate)

    def __init__(self, name=None, manager=None):
        self.name = self.__name__ = name
        self.manager = self.__parent__ = manager
        self.categories = []

    @property
    def services(self):
        return self.getServices()

    def getServices(self):
        svcs = self.getManager().getServices()
        categories = [c.strip() for c in self.categories if c.strip()]
        if categories:
            svcs = Jeep((key, s) for key, s in svcs.items()
                                 if s.category in categories)
        return svcs

    def getManager(self):
        return self.manager


class ClientRegistrations(object):

    implements(IClientRegistrations)
    adapts(IClient)

    template = None

    registrationsAttributeName = '__service_registrations__'

    errors = None
    severity = 0

    def __init__(self, context):
        self.context = context

    def register(self, services, numbers=None):
        if numbers is None:
            numbers = len(services) * [1]
        regs = [service.register(self.context, numbers[idx])
                for idx, service in enumerate(services)]
        old = getattr(self.context, self.registrationsAttributeName, [])
        regs.extend(r for r in old if r.service not in services)
        setattr(self.context, self.registrationsAttributeName, regs)

    def unregister(self, services):
        old = getattr(self.context, self.registrationsAttributeName, [])
        regs = [r for r in old if r.service not in services]
        setattr(self.context, self.registrationsAttributeName, regs)
        for service in services:
            service.unregister(self.context)

    def getRegistrations(self):
        regs = getattr(self.context, self.registrationsAttributeName, [])
        if self.template is not None:
            svcs = self.template.getServices().values()
            regs = [r for r in regs if r.service in svcs]
        return regs

    def validate(self, clientName, services, numbers=None):
        self.errors = {}
        if numbers is None:
            numbers = len(services) * [1]
        for svc, n in zip(services, numbers):
            if clientName:
                oldReg = svc.registrations.get(clientName, None)
                if oldReg is None or IStateful(oldReg).state == 'temporary':
                    # availableCapacity does not consider temporary registrations
                    oldN = 0
                else:
                    oldN = oldReg.number or 0
            else:
                oldN = 0
            if (not svc.waitingList and svc.capacity and svc.capacity > 0
                    and svc.availableCapacity < n - oldN):
                error = registrationErrors['capacity_exceeded']
                entry = self.errors.setdefault(svc.token, [])
                entry.append(error)
                self.severity = max(self.severity, error.severity)


class RegistrationError(object):

    def __init__(self, title, description=None, severity=5, **kw):
        self.title = title
        self.description = description or title
        self.severity = severity
        for k, v in kw.items():
            setattr(self, k, v)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "RegistrationError('%s')" % self.title


registrationErrors = dict(
    capacity_exceeded=RegistrationError(
            u'The capacity for this service has been exceeded.'),
    time_conflict=RegistrationError(
            u'You have registered already for another service at the same time.'),
    number_exceeded=RegistrationError(
            u'The total number of participants you are registering is less than the '
                'number of persons you want to register for this service.'),
)


# registration states

registrationStates = 'organize.service.registration'

registerStatesDefinition(
    StatesDefinition(registrationStates,
        State('temporary', 'temporary', ('submit', 'setwaiting', 'cancel',)),
        State('submitted', 'submitted',
                    ('change', 'retract', 'setwaiting', 'confirm', 'reject',)),
        State('cancelled', 'cancelled', ('activate',)),
        State('retracted', 'retracted', ('activate', 'cancel',)),
        State('waiting', 'waiting',
                    ('activate', 'change', 'retract', 'confirm', 'reject',)),
        State('confirmed', 'confirmed',
                    ('change', 'retract', 'reject',)),
        State('rejected', 'rejected',
                    ('change', 'retract', 'setwaiting', 'confirm',)),
        Transition('cancel', 'Cancel registration', 'cancelled'),
        Transition('submit', 'Submit registration', 'submitted'),
        Transition('change', 'Change registration', 'submitted'),
        Transition('retract', 'Retract registration', 'retracted'),
        Transition('setwaiting', 'Set on waiting list', 'waiting'),
        Transition('activate', 'Activate waiting or cancelled registration',
                    'temporary'),
        Transition('confirm', 'Confirm registration', 'confirmed'),
        Transition('reject', 'Reject registration', 'rejected'),
        initialState='temporary',
))


class StatefulRegistration(StatefulAdapter):

    component.adapts(IRegistration)

    statesDefinition = registrationStates


# events, rules, actions

eventTypes = Jeep((
    EventType('service.checkout'),
))


class RuleManagerAdapter(RuleManager):

    adapts(IServiceManager)

    def __init__(self, context):
        self.context = context


class MessageManagerAdapter(MessageManager):

    adapts(IServiceManager)

    def __init__(self, context):
        self.context = context

    def addMessage(self, messageName, text, **kw):
        super(MessageManagerAdapter, self).addMessage(messageName, text, **kw)
        self.context.messages = self.messages

    @Lazy
    def messages(self):
        return self.context.messages


def getCheckoutRule(sender):
    """ A rule for sending a confirmation message, provided by default.
    """
    checkoutRule = Rule('checkout')
    checkoutRule.events.append(eventTypes['service.checkout'])
    checkoutRule.actions.append(Action('sendmail',
                      parameters=dict(sender=sender,
                                      messageName='feedback_text')))
    checkoutRule.actions.append(Action('redirect',
                      parameters=dict(viewName='message_view.html',
                                      messageName='feedback_html',
                                      clearClient=True)))
    return checkoutRule


# Zope event handlers

def clientRemoved(obj, event):
    """ Handle removal of a client object.
    """
    regs = IClientRegistrations(obj)
    for r in regs.getRegistrations():
        r.service.unregister(obj)

def serviceRemoved(obj, event):
    """ Handle removal of a service.
    """
    for r in list(obj.registrations.values()):
        regs = IClientRegistrations(r.client)
        regs.unregister([obj])

