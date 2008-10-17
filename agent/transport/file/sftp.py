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

CHUNKSIZE = 4096


class FileTransfer(protocol.ClientFactory):
    """ Transfers files to a remote SCP/SFTP server.
    """
    channel = None

    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        self.queue = []
        reactor.connectTCP(host, port, self)

    def buildProtocol(self, addr):
        protocol = self.protocol = ClientTransport(self)
        return protocol

    def upload(self, localPath, remotePath):
        """ Copies a file, returning a deferred.
        """
        d = self.deferred = defer.Deferred()
        # we put everything in a queue so that more than one file may
        # be transferred in one connection.
        self.queue.append(dict(deferred=d,
                               command='upload',
                               localPath=localPath,
                               remotePath=remotePath))
        if len(self.queue) == 1 and self.channel is not None:
            # the channel has emptied the queue
            self.channel.execute()
        return d

    def close(self):
        # TODO: put in queue...
        self.protocol.transport.loseConnection()
        print 'connection closed'


class SFTPChannel(channel.SSHChannel):
    """ An SSH channel using the SFTP subsystem for transferring files
        and issuing other filesystem requests.
    """

    name = 'session'
    remFile = ''
    remOffset = 0

    def channelOpen(self, data):
        d = self.conn.sendRequest(self, 'subsystem', common.NS('sftp'), wantReply=1)
        d.addCallback(self.channelOpened)

    def channelOpened(self, data):
        self.client = filetransfer.FileTransferClient()
        self.client.makeConnection(self)
        self.dataReceived = self.client.dataReceived
        self.execute()
        self.conn.factory.channel = self

    def execute(self):
        queue = self.conn.factory.queue
        if queue:
            command = queue.pop()
            commandName = command.pop('command')
            method = getattr(self, 'command_' + commandName, None)
            if method is not None:
                self.params = command
                method()

    def command_upload(self):
        params = self.params
        remotePath = params['remotePath']
        localPath = params['localPath']
        self.localFile = open(localPath, 'rb')
        d = self.client.openFile(remotePath,
                    filetransfer.FXF_WRITE | filetransfer.FXF_CREAT, {})
        d.addCallbacks(self.writeChunk, self.logError)

    def writeChunk(self, remoteFile):
        if isinstance(remoteFile, tuple) == False:
            self.remFile = remoteFile
        data = self.localFile.read(CHUNKSIZE)
        if len(data) < CHUNKSIZE:
            self.d = self.remFile.writeChunk(self.remOffset, data)
            self.d.addCallbacks(self.finished, self.logError)
        else:
            self.d = self.remFile.writeChunk(self.remOffset, data)
            self.remOffset = self.remOffset + CHUNKSIZE
            self.d.addCallbacks(self.writeChunk, self.logError)

    def logError(self, reason):
        print 'error', reason

    def finished(self, result):
        self.localFile.close()
        self.remFile.close()
        #self.d.callback('finished')
        self.conn.factory.deferred.callback('finished')

# classes for managing the SSH protocol and connection

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


class UserAuth(userauth.SSHUserAuthClient):

    def __init__(self, factory, connection):
        userauth.SSHUserAuthClient.__init__(self, factory.username, connection)
        self.password = factory.password

    def getPassword(self, prompt=None):
        return defer.succeed(self.password)
