#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Handling asynchronous communication tasks - common and base classes.

$Id$
"""

from twisted.web.client import getPage
from zope.interface import implements

from cybertools.agent.talk.interfaces import ISession, IInteraction
from cybertools.util import json


class Session(object):

    implements(ISession)

    def __init__(self, id, manager, subscriber, url):
        self.id = id
        self.manager = manager
        self.subscriber = subscriber
        self.url = url
        self.state = 'logon'
        self.sending = False
        self.queue = []
        self.interactions = {}
        self.interactionCount = 0

    def received(self, data):
        data = json.loads(data)
        # TODO: check data; notify sender?
        self.sending = False
        self._processQueue()

    def send(self, data, interaction):
        data['interaction'] = interaction.id
        if self.sending or self.queue:
            self.queue.append(data)
        else:
            self._sendData(data)

    def processQueue(self):
        if not self.queue:
            return
        self._sendData(self.queue.pop(0))

    def sendData(self, data, command='send'):
        self.sending = True
        content = dict(id=self.id, command=command, data=data)
        d = getPage(self.url, postdata=json.dumps(content))
        d.addCallback(s.received)

    def connected(self, data):
        data = json.loads(data)
        self.state = 'open'
        self.subscriber.onMessage(None, data)
        self.sending = False
        self.processQueue()

    def generateInteractionId(self):
        self.interactionCount += 1
        return '%07i' % self.interactionCount


class Interaction(object):

    implements(IInteraction)

    finished = False

    def __init__(self, session):
        self.session = session
        self.id = self.session.generateInteractionId()
        self.session.interactions[self.id] = self

