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

from BTrees.OOBTree import OOBTree
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import implements
from cybertools.composer.interfaces import IInstance
from cybertools.util.jeep import Jeep

from cybertools.composer.schema.interfaces import IClientManager, IClient
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

    clientNum = 0

    def __init__(self):
        if self.servicesFactory is not None:
            self.services = self.servicesFactory()
        if self.clientSchemasFactory is not None:
            self.clientSchemas = self.clientSchemasFactory()

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
        self.clientNum += 1
        return '%05i' % self.clientNum


class Service(object):

    implements(IService)

    registrationsFactory = OOBTree

    def __init__(self, name=None, capacity=-1):
        self.name = name
        self.capacity = capacity
        if self.registrationsFactory is not None:
            self.registrations = self.registrationsFactory()

    @property
    def token(self):
        return self.name

    @property
    def availableCapacity(self):
        if self.capacity >= 0 and len(self.registrations) >= self.capacity:
            return 0
        return self.capacity - len(self.registrations)

    def register(self, client):
        clientName = client.__name__
        if clientName in self.registrations:
            return self.registrations[clientName]
        if self.availableCapacity:
            reg = Registration(client, self)
            self.registrations[clientName] = reg
            return reg
        return None

    def unregister(self, client):
        clientName = client.__name__
        if clientName in self.registrations:
            del self.registrations[clientName]


class ScheduledService(Service):

    implements(IScheduledService)


# registration

class Registration(object):

    implements(IRegistration)

    def __init__(self, client, service):
        self.client = client
        self.service = service


class RegistrationTemplate(object):

    implements(IRegistrationTemplate)

    def __init__(self, name=None, manager=None):
        self.name = name
        self.manager = manager

    @property
    def services(self):
        return self.manager.services

    def getManager(self):
        return self.manager


class ClientRegistrations(object):

    implements(IClientRegistrations)
    adapts(IClient)

    template = None

    def __init__(self, context):
        self.context = context

    def register(self, services):
        for service in services:
            service.register(self.context)

    def unregister(self, services):
        for service in services:
            service.unregister(self.context)

    def getRegistrations(self):
        for service in self.template.services:
            for reg in service.registrations.values():
                if self.context == reg.client:
                    yield reg

