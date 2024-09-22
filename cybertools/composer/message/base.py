# cybertools.composer.message.base

""" Basic classes for message management.
"""

from zope.interface import implementer

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.message.interfaces import IMessageManager, IMessage
from cybertools.util.jeep import Jeep


@implementer(IMessageManager)
class MessageManager(object):

    messagesFactory = Jeep

    messages = None
    manager = None

    def getManager(self):
        return self.manager

    def addMessage(self, messageName, text, **kw):
        message = Message(messageName, manager=self, **kw)
        message.text = text
        if self.messages is None:
            self.messages = self.messagesFactory()
        self.messages.append(message)


@implementer(IMessage)
class Message(Template):

    name = u''
    manager = None

    def __init__(self, name, text=u'', subjectLine=u'', **kw):
        self.name = name
        self.text = text
        self.subjectLine = subjectLine
        for k, v in kw.items():
            setattr(self, k, v)

