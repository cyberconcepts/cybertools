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
Transferring files to a remote site via SCP.

$Id$
"""

from twisted.conch.ssh import connection
from twisted.conch.ssh import filetransfer, transport, userauth
from twisted.internet import defer, protocol, reactor


class FileTransferConnection(protocol.ClientFactory):
    """ Transfers files to a remote SCP server.
    """

    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        self.queue = []
        reactor.connectTCP(host, port, self)

    def buildProtocol(self, addr):
        protocol = self.protocol = ClientTransport(self.username, self.password)
        return protocol

    def copyToRemote(self, localPath, remotePath):
        """ Copies a file, returning a deferred.
        """
        d = defer.Deferred()
        self.queue.append((localPath, remotePath, d))
        #d = self.protocol.openFile('text.txt', filetransfer.FXF_WRITE, {})
        #d.addCallback(self.write)
        return d

    def write(self, file):
        file.writeChunk(0, 'hello')
        file.close()
        return 'Done'

    def close(self):
        self.protocol.transport.loseConnection()
        print 'connection closed'


class ClientTransport(transport.SSHClientTransport):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verifyHostKey(self, pubKey, fingerprint):
        # this is insecure!!!
        return defer.succeed(True)

    def connectionSecure(self):
        self.requestService(UserAuth(self.username, self.password,
                                     ClientConnection()))


class ClientConnection(connection.SSHConnection):

    def serviceStarted(self):
        self.openChannel(SFTPChannel(conn=self))


class SFTPChannel(channel.SSHChannel):

    def channelOpened(self, data):
        self.client = filetransfer.FileTransferClient


class UserAuth(userauth.SSHUserAuthClient):

    def __init__(self, user, password, connection):
        userauth.SSHUserAuthClient.__init__(self, user, connection)
        self.password = password

    def getPassword(self, prompt=None):
        return defer.succeed(self.password)
