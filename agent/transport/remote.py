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
from cybertools.agent.system import rpcapi

from cybertools.agent.base.agent import Master
from cybertools.agent.core.agent import QueueableAgent
from cybertools.agent.interfaces import ITransporter
from cybertools.agent.crawl.base import Metadata
from cybertools.agent.crawl.mail import MailResource
from cybertools.agent.crawl.filesystem import FileResource
from cybertools.agent.components import agents
from cybertools.util.config import Configurator


class Transporter(QueueableAgent):

    implements(ITransporter)
    
    serverURL = ''
    server = ''
    method = ''
    machineName = ''
    userName = ''
    password = ''
    resource = None

    def __init__(self, master, params):
        super(Transporter, self).__init__(master)
##        if isinstance(configuration, Configurator):
##            self.config = configuration
##        else:   # configuration is path to config file
##            self.config = Configurator()
##            self.config.load(configuration)
        self.serverURL = params[serverURL]
        self.server = rpcapi.xmlrpc.Proxy(self.serverURL)
        self.method = params[method]
        self.machineName = params[machineName]
        self.userName = params[userName]
        self.password = params[password]

    def transfer(self, resource):
        """ Transfer the resource (an object providing IResource)
            to the server and return a Deferred.
        """
        deferred = self.server.callRemote('getMetadata', resource.metadata)
        deferred.addCallback(self.transferDone)
        deferred.addErrback(self.errorHandler)
    
    def errorHandler(self, errorInfo):
        """
        Invoked as a callback from self.transfer
        Error handler.
        """
        print errorInfo
        self.server.close()
        
    def transferDone(self, successMessage=''):
        """
        Invoked as a callback from self.transfer
        This callback method is called when resource and metadata
        have been transferred successfully.
        """
        print successMessage
        pass

#    def process(self):
#        return self.collect()

#    def collect(self, filter=None):
#        d = defer.succeed([])
#        return d

agents.register(Transporter, Master, name='transport.remote')