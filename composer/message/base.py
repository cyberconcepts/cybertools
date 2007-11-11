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
Basic classes for message management.

$Id$
"""

from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.message.interfaces import IMessageManager, IMessage
from cybertools.util.jeep import Jeep


class MessageManager(object):

    implements(IMessageManager)

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


class Message(Template):

    implements(IMessage)

    name = u''
    manager = None

    def __init__(self, name, text=u'', subjectLine=u'', **kw):
        self.name = name
        self.text = text
        self.subjectLine = subjectLine
        for k, v in kw.items():
            setattr(self, k, v)

