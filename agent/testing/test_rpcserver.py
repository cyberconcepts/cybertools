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
Providing access for remote agent instances by listening for requests
from remote transport agents.

$Id$
"""

from twisted.web import xmlrpc, server, resource
from twisted.internet import defer, reactor
from cybertools.agent.base.agent import Agent

application = None

class RPCServer(xmlrpc.XMLRPC):

    serverURL = ''
    method = ''
    machineName = ''
    userName = ''
    password = ''
    controller = ''
    close = reactor.stop

    def __init__(self, serverURL = '', method = '', machineName = '',
                 userName = '', password = '', controlObj= None):
        self.serverURL = serverURL
        self.method = method
        self.machineName = machineName
        self.userName = userName
        self.password = password
        self.controller = controlObj
        xmlrpc.XMLRPC.__init__(self)

    def xmlrpc_transfer(self, resource):
        if self.controller is not None:
            # pass resource object to controller
            # this is done BEFORE the metadata is handed over
            # call notify method of controller
            pass
        print resource
        return "Resource received: ", resource

    def xmlrpc_getMetadata(self, metadata):
        if self.controller is not None:
            # pass metadata to controller
            # this is done AFTER the resource (like e.g. file or mail)
            # is handed over
            pass
        print '*** metadata', metadata
        metadata = "Echo: ", metadata
        return metadata

    def xmlrpc_shutdownRPCServer():
        self.close()


if __name__ == '__main__':
    from twisted.internet import reactor
    site = RPCServer()
    reactor.listenTCP(8082, server.Site(site))
    print '*** listening...'
    reactor.run()