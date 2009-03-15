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

from twisted.internet import defer
from twisted.web.client import getPage
from twisted.web.resource import Resource
from twisted.web.server import Site
from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.components import servers, clients
from cybertools.agent.system.http import listener
from cybertools.agent.talk.base import Session, Interaction
from cybertools.agent.talk.interfaces import IServer, IClient


# server implementation

#@server
class HttpServer(object):

    implements(IServer)

    def __init__(self, agent):
        self.agent = agent
        self.port = agent.config.talk.server.http.port
        self.subscribers = {}
        self.sessions = {}
        self.site = Site(RootResource())

    def setup(self):
        print 'Setting up HTTP handler for port %i.' % self.port
        listener.listenTCP(self.port, self.site)

    def subscribe(self, subscriber, aspect):
        pass

    def unsubscribe(self, subscriber, aspect):
        pass

    def send(self, session, data, interaction=None):
        # respond to open poll request or put in queue
        return defer.Deferred() # Interaction

servers.register(HttpServer, Master, name='http')


class RootResource(Resource):

    def getChild(self, path, request):
        return CommandHandler(path)


class CommandHandler(Resource):

    def __init__(self, path):
        self.command = path

    def render(self, request):
        #print request
        return '{"message": "OK"}'


# client implementation

#@client
class HttpClient(object):

    implements(IClient)

    def __init__(self, agent):
        self.agent = agent
        self.sessions = {}

    def connect(self, subscriber, url, credentials=None):
        s = Session(self)
        d = getPage(url)
        d.addCallback(s.receive)
        return s

    def disconnect(self, session):
        pass

    def send(self, session, data, interaction=None):
        return defer.Deferred() # Interaction

clients.register(HttpClient, Master, name='http')
