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
Transferring files to a remote site via SFTP.

$Id$
"""

from twisted.conch.ssh import channel, common, connection
from twisted.conch.ssh import filetransfer, transport, userauth
from twisted.internet import defer, protocol, reactor


class FileTransfer(protocol.ClientFactory):
    """ Transfers files to a remote SCP/SFTP server.
    """

    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        self.queue = []
        reactor.connectTCP(host, port, self)

    def buildProtocol(self, addr):
        protocol = self.protocol = ClientTransport(self)
        return protocol

    def copyToRemote(self, localPath, remotePath):
        """ Copies a file, returning a deferred.
        """
        d = defer.Deferred()
        self.queue.append(dict(deferred=d,
                               command='copyToRemote',
                               localPath=localPath,
                               remotePath=remotePath))
        return d

    def close(self):
        # TODO: put in queue...
        self.protocol.transport.loseConnection()
        print 'connection closed'


class ClientTransport(transport.SSHClientTransport):

    def __init__(self, factory):
        self.factory = factory

    def verifyHostKey(self, pubKey, fingerprint):
        # this is insecure!!!
        return defer.succeed(True)

    def connectionSecure(self):
        self.requestService(UserAuth(self.factory, ClientConnection(self.factory)))


class ClientConnection(connection.SSHConnection):

    def __init__(self, factory):
        connection.SSHConnection.__init__(self)
        self.factory = factory

    def serviceStarted(self):
        self.openChannel(SFTPChannel(conn=self))


class SFTPChannel(channel.SSHChannel):

    name = 'session'

    def channelOpen(self, data):
        d = self.conn.sendRequest(self, 'subsystem', common.NS('sftp'), wantReply=1)
        d.addCallback(self.channelOpened)

    def channelOpened(self, data):
        print 'channelOpened', data
        self.client = filetransfer.FileTransferClient()
        self.client.makeConnection(self)
        self.dataReceived = self.client.dataReceived
        self.execute()

    def execute(self):
        queue = self.conn.factory.queue
        print 'execute, queue =', queue

    def copyToRemote(self, params):
        remotePath = params['remotePath']
        d = self.protocol.openFile(remotePath, filetransfer.FXF_WRITE, {})


class UserAuth(userauth.SSHUserAuthClient):

    def __init__(self, factory, connection):
        userauth.SSHUserAuthClient.__init__(self, factory.username, connection)
        self.password = factory.password

    def getPassword(self, prompt=None):
        return defer.succeed(self.password)
