#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Handling asynchronous and possibly asymmetric communication tasks via HTTP.

$Id$
"""

from time import time
from twisted.web.client import getPage
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.components import servers, clients
from cybertools.agent.system.http import listener
from cybertools.agent.talk.base import Session, Interaction
from cybertools.agent.talk.interfaces import IServer, IClient
from cybertools.util import json


# server implementation

#@server
class HttpServer(object):

    implements(IServer)

    def __init__(self, agent):
        self.agent = agent
        self.port = agent.config.talk.server.http.port
        self.subscribers = {}
        self.sessions = {}
        self.site = Site(RootResource(self))

    def setup(self):
        print 'Setting up HTTP handler for port %i.' % self.port
        listener.listenTCP(self.port, self.site)

    def subscribe(self, subscriber, aspect):
        subs = self.subscribers.setdefault(aspect, [])
        if subscriber not in subs:
            subs.append(subscriber)

    def unsubscribe(self, subscriber, aspect):
        pass

    def send(self, session, data, interaction=None):
        if interaction is None:
            interaction = Interaction(session)
        # check session's queue
        # check open poll - write response
        return interaction

    def process(self, client, data):
        action = data.get('action')
        if not action:
            return self._error('missing action')
        amethod = self.actions.get(action)
        if amethod is None:
            return self._error('illegal action %r' % action)
        sid = data.get('session')
        if not sid:
            return self._error('missing session id')
        sessionId = ':'.join((client, sid))
        message = amethod(self, sessionId, client, data)
        if message:
            return self._error(message)
        return '{"status": "OK"}'

    def _connect(self, sessionId, client, data):
        if sessionId in self.sessions:
            return 'duplicate session id %r' % sessionId
        self.sessions[sessionId] = HttpServerSession(sessionId, self, None, client)
        # TODO: notify subscribers

    def _poll(self, sessionId, client, data):
        # record deferred with session
        return NOT_DONE_YET

    def _send(self, sessionId, client, data):
        for sub in self.subscribers.values():
            sub.onMessage(data)

    def _error(self, message):
        return json.dumps(dict(status='error', message=message))

    actions = dict(connect=_connect, poll=_poll, send=_send)

servers.register(HttpServer, Master, name='http')


class RootResource(Resource):

    isLeaf = True

    def __init__(self, server):
        self.server = server

    def render(self, request):
        client = request.getClient()
        data = json.loads(request.content.read())
        return self.server.process(client, data)


class HttpServerSession(Session):

    pass


# client implementation

#@client
class HttpClient(object):

    implements(IClient)

    def __init__(self, agent):
        self.agent = agent
        self.sessions = {}

    def connect(self, subscriber, url, credentials=None):
        id = self.generateSessionId()
        s = HttpClientSession(self, id, subscriber, url)
        self.sessions[id] = s
        data = dict(action='connect', session=id)
        if credentials is not None:
            data.update(credentials)
        # s.send(data, None)
        d = getPage(url, postdata=json.dumps(data))
        d.addCallback(s.connected)
        return s

    def disconnect(self, session):
        pass

    def send(self, session, data, interaction=None):
        if interaction is None:
            interaction = Interaction(session)
        session.send(data, interaction)
        return interaction

    def generateSessionId(self):
        return '%.7f' % time()

clients.register(HttpClient, Master, name='http')


class HttpClientSession(Session):

    def connected(self, data):
        super(HttpClientSession, self).connected(data)
        # self.poll()

    def pollReceived(self, data):
        data = json.loads(data)
        if data.get('action') != 'idle':
            self.subscriber.onMessage(interaction, data)
        # self.poll()

    def poll(self):
        content = dict(id=self.id, command='poll')
        d = getPage(self.url, postdata=json.dumps(content))
        d.addCallback(s.pollReceived)
