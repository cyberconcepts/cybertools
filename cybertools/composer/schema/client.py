# cybertools.composer.schema.client

""" Client implementations.
"""

from BTrees.OOBTree import OOBTree
from persistent import Persistent
from time import time
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.interface import implementer

from cybertools.composer.message.base import MessageManager
from cybertools.composer.rule.base import RuleManager, EventType
from cybertools.composer.rule.base import Rule, Action
from cybertools.composer.schema.interfaces import IClient
from cybertools.composer.schema.interfaces import IClientManager, IClientFactory
from cybertools.stateful.base import StatefulAdapter
from cybertools.stateful.definition import registerStatesDefinition
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.util.jeep import Jeep
from cybertools.util.randomname import generateName


@implementer(IClientManager)
class ClientManager(object):

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


@implementer(IClient)
class Client(Persistent):

    timeStamp = None

    def __init__(self, manager=None):
        self.manager = manager
        self.timeStamp = int(time())


@implementer(IClientFactory)
class ClientFactory(object):

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


# registration states

clientStates = 'composer.schema.client'

registerStatesDefinition(
    StatesDefinition(clientStates,
        State('temporary', 'temporary', ('submit', 'cancel',)),
        State('submitted', 'submitted',
                    ('change', 'retract', 'confirm', 'reject',)),
        State('cancelled', 'cancelled', ('activate',)),
        State('retracted', 'retracted', ('activate', 'cancel',)),
        State('confirmed', 'confirmed',
                    ('change', 'retract', 'reject',)),
        State('rejected', 'rejected',
                    ('change', 'retract', 'confirm',)),
        Transition('cancel', 'Cancel registration', 'cancelled'),
        Transition('submit', 'Submit registration', 'submitted'),
        Transition('change', 'Change registration', 'submitted'),
        Transition('retract', 'Retract registration', 'retracted'),
        Transition('activate', 'Activate cancelled registration',
                    'temporary'),
        Transition('confirm', 'Confirm registration', 'confirmed'),
        Transition('reject', 'Reject registration', 'rejected'),
        initialState='temporary',
))


class StatefulClient(StatefulAdapter):

    adapts(IClient)

    statesDefinition = clientStates


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

