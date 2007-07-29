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

from cybertools.organize.interfaces import IServiceManager
from cybertools.organize.interfaces import IClient, IClientFactory
from cybertools.organize.interfaces import IService, IScheduledService


class ServiceManager(object):

    implements(IServiceManager)

    servicesFactory = list
    clientSchemasFactory = Jeep
    clientsFactory = OOBTree

    clientNum = 0

    def __init__(self):
        if self.servicesFactory is not None:
            self.services = self.servicesFactory()
        if self.clientSchemasFactory is not None:
            self.clientSchemas = self.clientSchemasFactory()

    @Lazy
    def clients(self):
        return self.clientsFactory()

    def addClient(self, client):
        name = self.generateClientName(client)
        self.clients[name] = client

    def generateClientName(self, client):
        self.clientNum += 1
        return '%05i' % self.clientNum


class Service(object):

    implements(IService)

    def __init__(self, capacity=-1):
        self.capacity = capacity
        self.registrations = []

    @property
    def availableCapacity(self):
        if self.capacity >= 0 and len(self.registrations) >= self.capacity:
            return 0
        return self.capacity - len(self.registrations)

    def register(self, client):
        if self.availableCapacity:
            reg = Registration(client)
            self.registrations.append(reg)
            return reg
        return None


class ScheduledService(Service):

    implements(IScheduledService)


class Client(object):

    implements(IClient)

    def __init__(self, manager):
        self.manager = manager


class ClientFactory(object):

    implements(IClientFactory)
    adapts(IServiceManager)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return Client(self.context)


class ClientInstanceAdapter(object):

    implements(IInstance)
    adapts(IClient)

    baseAspect = 'service.client.'
    schema = 'default'

    @property
    def aspect(self):
        return self.baseAspect + self.schema

    @property
    def template(self):
        return self.context.manager.clientSchemas.get(self.schema, None)

    def __init__(self, context):
        self.context = context

    def applyTemplate(self, data={}, schema='default', **kw):
        if getattr(self.context, 'attributes', None) is None:
            self.context.attributes = OOBTree()
        self.schema = schema
        template = self.template
        attributes = self.context.attributes.setdefault(self.aspect, OOBTree())
        if template is not None:
            for c in template.components:
                name = c.name
                attributes[name] = data.get(name, u'')


class Registration(object):

    def __init__(self, client):
        self.client = client

