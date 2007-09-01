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
from cybertools.composer.schema.interfaces import IClientManager, IClient
from cybertools.stateful.definition import registerStatesDefinition
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.util.jeep import Jeep
from cybertools.util.randomname import generateName
from cybertools.organize.interfaces import IServiceManager
from cybertools.organize.interfaces import IService, IScheduledService
from cybertools.organize.interfaces import IRegistration, IRegistrationTemplate
from cybertools.organize.interfaces import IClientRegistrations


class ServiceManager(object):

    implements(IServiceManager, IClientManager)

    servicesFactory = Jeep
    clientSchemasFactory = Jeep
    clientsFactory = OOBTree

    services = None
    clients = None

    def __init__(self):
        if self.servicesFactory is not None:
            self.services = self.servicesFactory()
        if self.clientSchemasFactory is not None:
            self.clientSchemas = self.clientSchemasFactory()

    def getServices(self):
        return self.services

    def getClientSchemas(self):
        return self.clientSchemas

    @Lazy
    def clients(self):
        return self.clientsFactory()

    def getClients(self):
        return self.clients

    def addClient(self, client):
        name = self.generateClientName(client)
        self.clients[name] = client
        client.__name__ = name
        return name

    def generateClientName(self, client):
        return generateName(self.checkClientName)

    def checkClientName(self, name):
        return name not in self.getClients()


class Service(object):

    implements(IService)

    registrationsFactory = OOBTree

    manager = None
    category = None
    allowRegWithNumber = False

    def __init__(self, name=None, title=u'', capacity=-1, **kw):
        self.name = self.__name__ = name
        self.title = title
        self.capacity = capacity
        if self.registrationsFactory is not None:
            self.registrations = self.registrationsFactory()
        self.classification = []
        for k, v in kw.items():
            setattr(self, k, v)

    def getName(self):
        return self.name

    def getManager(self):
        return self.manager

    def getClassification(self):
        return self.classification

    def getCategory(self):
        return self.category

    @property
    def token(self):
        return self.getToken()

    def getToken(self):
        return self.name

    @property
    def availableCapacity(self):
        if self.capacity >= 0 and len(self.registrations) >= self.capacity:
            return 0
        return self.capacity - len(self.registrations)

    def register(self, client, number=1):
        clientName = client.__name__
        if clientName in self.registrations:
            reg = self.registrations[clientName]
            if number != reg.number:
                reg.number = number
                self.registrations[clientName] = reg # persistence hack
            return reg
        reg = Registration(client, self, number)
        self.registrations[clientName] = reg
        return reg
        #if self.availableCapacity:
        # TODO: handle case when no capacity available -
        #       probably on 'submit' transition; UI feedback?

    def unregister(self, client):
        clientName = client.__name__
        if clientName in self.registrations:
            del self.registrations[clientName]


class ScheduledService(Service):

    implements(IScheduledService)

    start = end = None

    def getStartFromManager(self):
        return getattr(self.getManager(), 'start', None)
    def getEndFromManager(self):
        return getattr(self.getManager(), 'end', None)


# registration

class Registration(object):

    implements(IRegistration)

    number = 1

    def __init__(self, client, service, number=1):
        self.client = client
        self.service = service
        self.timeStamp = int(time())
        self.number = number


class RegistrationTemplate(object):

    implements(IRegistrationTemplate)

    def __init__(self, name=None, manager=None):
        self.name = self.__name__ = name
        self.manager = self.__parent__ = manager

    @property
    def services(self):
        return self.getServices()

    def getServices(self):
        # TODO: Restrict according to the objects selection criteria
        return self.getManager().getServices()

    def getManager(self):
        return self.manager


class ClientRegistrations(object):

    implements(IClientRegistrations)
    adapts(IClient)

    template = None

    registrationsAttributeName = '__service_registrations__'

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
        return getattr(self.context, self.registrationsAttributeName, [])


# registration states definition

registerStatesDefinition(
    StatesDefinition('organize.service.registration',
        State('temporary', 'temporary', ('submit', 'cancel',)),
        State('submitted', 'submitted', ('retract', 'setwaiting', 'confirm', 'reject',)),
        State('cancelled', 'cancelled', ('submit',)),
        State('retracted', 'retracted', ('submit',)),
        State('waiting', 'waiting', ('retract', 'confirm', 'reject',)),
        State('confirmed', 'confirmed', ('retract', 'reject',)),
        State('rejected', 'rejected', ('retract', 'setwaiting', 'confirm',)),
        Transition('cancel', 'Cancel registration', 'cancelled'),
        Transition('submit', 'Submit registration', 'submitted'),
        Transition('retract', 'Retract registration', 'retracted'),
        Transition('setwaiting', 'Set on waiting list', 'waiting'),
        Transition('confirm', 'Confirm registration', 'confirmed'),
        Transition('reject', 'Reject registration', 'rejected'),
        initialState='temporary',
))


# event handlers

def clientRemoved(obj, event):
    """ Handle removal of a client object.
    """
    regs = IClientRegistrations(obj)
    for r in regs.getRegistrations():
        r.service.unregister(obj)
