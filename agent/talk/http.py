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
Handling asynchronous and possibly asymmetric communication tasks.

$Id$
"""

from twisted.internet import defer
from twisted.web.resource import Resource
from twisted.web.server import Site
from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.system.http import listener


class RootResource(Resource):

    def getChild(self, path, request):
        return CommandHandler(path)


class CommandHandler(Resource):

    def __init__(self, path):
        self.command = path

    def render(self, request):
        return '{"message": "OK"}'


class Handler(object):

    def listen(self, port):
        return listener.listenTCP(port, Site(RootResource()))

    def send(self, clientId, data):
        return defer.Deferred()
