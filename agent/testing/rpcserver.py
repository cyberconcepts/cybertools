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
Fake rpcserver for testing purposes

$Id$
"""

from twisted.internet.defer import succeed


class RPCServer(object):

    serverURL = ''
    method = ''
    machineName = ''
    userName = ''
    password = ''
    controller = ''

    def __init__(self, serverURL = '', method = '', machineName = '',
                 userName = '', password = '', controlObj= None):
        self.serverURL = serverURL
        self.method = method
        self.machineName = machineName
        self.userName = userName
        self.password = password
        self.controller = controlObj

    def getMetadata(self, metadata):
        if self.controller is not None:
            # pass metadata to controller
            # this is done AFTER the resource (like e.g. file or mail)
            # is handed over
            pass
        deferred = succeed('Metadata accepted by server')
        return deferred

    def xmlrpc_shutdownRPCServer():
        return "xmlrRPC server shutdown completed!"


class XmlRpc(object):

     Proxy = None
     XMLRPC = None
     Handler = None
     XMLRPCIntrospection = None
     QueryProtocol = None
     _QueryFactory = None

     def __init__(self):
         self.Proxy = Proxy
         #self.XMLRPC = XMLRPC()
         #self.Handler = Handler()
         #self.XMLRPCIntrospection = XMLRPCIntrospection()
         #self.QueryProtocol = QueryProtocol()
         #self._QueryFactory = _QueryFactory()

     def addIntrospection(self, xmlrpc):
         pass


class Proxy(object):

     url = ''
     user = None
     password = None
     allowNone = False
     queryFactory = None

     def __init__(self, url, user=None, password=None, allowNone=False):
         self.url = url
         self.user = user
         self.password = password
         self.allowNone = allowNone
         self.RPCServer = RPCServer()

     def callRemote(self, methodName, *params):
        """
        intended to simulate the callRemote command of a real xmlrpcserver
        that takes a method name and calls the method, returning the results
        as xml formatted strings
        """
        method = getattr(self.RPCServer, methodName)
        return method(*params)


xmlrpc = XmlRpc()


class XMLRPC(object):

    def __init__(self):
        pass


class Handler(object):

    def __init__(self):
        pass


class XMLRPCIntrospection(object):

    def __init__(self):
        pass


class QueryProtocol(object):

    def __init__(self):
        pass


class _QueryFactory(object):

    def __init__(self):
        pass
