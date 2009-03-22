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

from twisted.web.client import getPage
from twisted.web.resource import Resource
from twisted.web.server import Site
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
        # respond to open poll request or put in queue
        return defer.Deferred() # Interaction

    def _process(self, client, data):
        command = data.get('command')
        if not command:
            return self._error('missing command')
        cmethod = self.commands.get(command)
        if cmethod is None:
            return self._error('illegal command %r' % command)
        id = data.get('id')
        if not id:
            return self._error('missing id')
        sessionId = ':'.join((client, data['id']))
        message = cmethod(self, sessionId, client, data)
        if message:
            return self._error(message)
        return '{"status": "OK"}'

    def _connect(self, sessionId, client, data):
        if sessionId in self.sessions:
            return 'duplicate session id %r' % sessionId
        self.sessions[sessionId] = Session(sessionId, self, None, client)
        # TODO: notify subscribers

    def _poll(self, sessionId, client, data):
        pass

    def _send(self, sessionId, client, data):
        for sub in self.subscribers.values():
            sub.onMessage(data)

    def _error(self, message):
        return json.dumps(dict(status='error', message=message))

    commands = dict(connect=_connect, poll=_poll, send=_send)

servers.register(HttpServer, Master, name='http')


class RootResource(Resource):

    isLeaf = True

    def __init__(self, server):
        self.server = server

    def render(self, request):
        client = request.getClient()
        data = json.loads(request.content.read())
        return self.server._process(client, data)


# client implementation

#@client
class HttpClient(object):

    implements(IClient)

    def __init__(self, agent):
        self.agent = agent
        self.sessions = {}
        self.count = 0

    def connect(self, subscriber, url, credentials=None):
        id = self.generateSessionId()
        s = Session(self, id, subscriber, url)
        self.sessions[id] = s
        data = dict(command='connect', id=id)
        if credentials is not None:
            data.update(credentials)
        # s._send(data, None)
        d = getPage(url, postdata=json.dumps(data))
        d.addCallback(s.connected)
        return s

    def disconnect(self, session):
        pass

    def send(self, session, data, interaction=None):
        if interaction is None:
            interaction = Interaction(session)
        session._send(data, interaction)
        return interaction # Interaction

    def generateSessionId(self):
        self.count += 1
        return '%07i' % self.count

clients.register(HttpClient, Master, name='http')
