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
RPCClient takes over the task of transferring metadata to the
loops RPCServer (control.remote)
RPCClient is invoked by the transporter (transport.remote)

$Id$
"""

from twisted.web import xmlrpc
from twisted.internet import reactor

class RPCClient(object):
    
    close = reactor.stop
    server = None

    def __init__(self, url):
        self.server = xmlrpc.Proxy(url)
        reactor.run()
        
    def cb_printServerResponse(self, response=''):
        """
        this method is invoked by a callback
        """
        print response
        return response
    
    def cb_errorHandler(self, error):
        """
        this method is invoked by a callback
        """
        print error
        return error
        
    def transferMetadata(self, metadata):
        deferred = self.server.callRemote('getMetadata', metadata)
        deferred.addCallback(self.cb_printServerResponse)
        deferred.addErrback(self.cb_errorHandler)
        
    def transferResource(self, resource):
        deferred = self.server.callRemote('transfer', resource)
        deferred.addCallback(self.cb_printServerResponse)
        deferred.addErrback(self.cb_errorHandler)
        
    def printString(self):
        print "Client test function printString"


if __name__ == '__main__':
    url = 'http://localhost:8082'
    for elem in range(1,4):
        elem = "Testcounter: ", elem
        RPCClient(url).transferMetadata(elem)
    RPCClient(url).printString()
    reactor.run()
    