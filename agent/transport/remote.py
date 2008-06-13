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
Transferring information to or requesting information from a remote
cybertools.agent instance by transferring files to the remote system
and sending requests to a corresponding remote controller.

$Id$
"""

from zope.interface import implements

from cybertools.agent.core.agent import QueueableAgent
from cybertools.agent.interfaces import ITransporter
from cybertools.agent.transport.rpcclient import RPCClient
from cybertools.agent.crawl.base import Metadata
from cybertools.agent.crawl.mail import MailResource
from cybertools.agent.crawl.filesystem import FileResource


class Transporter(QueueableAgent):

    implements(ITransporter)
    
    serverURL = ''
    method = ''
    machineName = ''
    userName = ''
    password = ''
    xmlrpcClient = ''
    resource = None

    def __init__(self, master, params={}):
        super(Transporter, self).__init__(master)
        if params.has_key(serverURL):
            self.xmlrpcClient = RPCClient(self.serverURL)

    def transfer(self, resource):
        """ Transfer the resource (an object providing IResource)
            to the server and return a Deferred.
        """
        deferred = self.xmlrpcClient.transferResource(resource)
        # concept test method
        # sftp transfer here with callback to self.cb_sendMetadata
        deferred.addCallback(self.cb_sendMetadata)
        deferred.addErrback(self.cb_errorHandler)

    def cb_sendMetadata(self, serverResponse=''):
        """
        After the resource object has been sent successfully to the
        RPCServer this method is invoked by a callback from the
        transfer method and is sending the according metadata of the resource.
        """
        # maybe react here to a special server response like
        # e.g. delay because of server being in heavy load condition
        deferred = self.xmlrpcClient.transferMetadata(self.resource.metadata)
        deferred.addCallback(self.cb_transferDone)
        deferred.addErrback(self.cb_errorHandler)
    
    def cb_errorHandler(self, errorInfo):
        """
        This is a callback error Handler
        """
        print errorInfo
        self.xmlrpcClient.close()
        
    def cb_transferDone(self, successMessage=''):
        """
        This callback method is called when resource and metadata
        have been transferred successfully.
        """
        pass

#    def process(self):
#        return self.collect()

#    def collect(self, filter=None):
#        d = defer.succeed([])
#        return d

