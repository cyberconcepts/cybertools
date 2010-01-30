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
Client implementations.

$Id$
"""

from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import implements

from cybertools.composer.message.base import MessageManager
from cybertools.composer.rule.base import RuleManager, EventType
from cybertools.composer.rule.base import Rule, Action
from cybertools.composer.schema.interfaces import IClient
from cybertools.composer.schema.interfaces import IClientManager, IClientFactory
from cybertools.util.jeep import Jeep
from cybertools.util.randomname import generateName


class ClientManager(object):

    implements(IClientManager)

    clientSchemasFactory = Jeep
    clientsFactory = OOBTree

    clients = None

    messages = None

    senderEmail = 'unknown@sender.com'

    def __init__(self):
        if self.clientSchemasFactory is not None:
            self.clientSchemas = self.clientSchemasFactory()

    def isActive(self):
        return True

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


class Client(Persistent):

    implements(IClient)

    def __init__(self, manager=None):
        self.manager = manager


class ClientFactory(object):

    implements(IClientFactory)
    adapts(IClientManager)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return Client(self.context)


class MessageManagerAdapter(MessageManager):

    adapts(IClientManager)

    def __init__(self, context):
        self.context = context

    def addMessage(self, messageName, text, **kw):
        super(MessageManagerAdapter, self).addMessage(messageName, text, **kw)
        self.context.messages = self.messages

    @Lazy
    def messages(self):
        return self.context.messages


class RuleManagerAdapter(RuleManager):

    adapts(IClientManager)

    def __init__(self, context):
        self.context = context


eventTypes = Jeep((
    EventType('client.checkout'),
))


def getCheckoutRule(sender):
    """ A rule for sending a confirmation message, provided by default.
    """
    checkoutRule = Rule('checkout')
    checkoutRule.events.append(eventTypes['client.checkout'])
    checkoutRule.actions.append(Action('sendmail',
                      parameters=dict(sender=sender,
                                      messageName='feedback_text')))
    checkoutRule.actions.append(Action('redirect',
                      parameters=dict(viewName='message_view.html',
                                      messageName='feedback_html',
                                      clearClient=True)))
    return checkoutRule

