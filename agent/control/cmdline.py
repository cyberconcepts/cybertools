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
Base/sample controller implementation.

$Id$
"""

from twisted.application import service, internet
from twisted.internet import protocol, reactor, stdio
from twisted.protocols import basic
from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.core.control import SampleController
from cybertools.agent.components import controllers


class CmdlineController(SampleController):

    def setup(self):
        super(CmdlineController, self).setup()
        prot = CmdlineProtocol()
        prot.controller = self
        stdio.StandardIO(prot)

controllers.register(CmdlineController, Master, name='cmdline')


class TelnetController(CmdlineController):

    def setup(self):
        super(CmdlineController, self).setup()
        port = self.agent.config.controller.telnet.port
        from cybertools.agent.main import application
        if application is None:
            reactor.listenTCP(port, TelnetServerFactory(self))
        else:
            service = internet.TCPServer(port, TelnetServerFactory(self))
            service.setServiceParent(application)

controllers.register(TelnetController, Master, name='telnet')


class CmdlineProtocol(basic.LineReceiver):

    delimiter = '\n'
    controller = None

    def connectionMade(self):
        self.sendLine("Agent console. Type 'help' for help.")
        self.transport.write('> ')

    def lineReceived(self, line):
        if not line:
            return
        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]
        posArgs = []
        kwArgs = {}
        for arg in args:
            if '=' in arg:  # directory='...'
                key, value = arg.split('=', 1)
                if value in ('True', 'False'):
                    value = eval(value)
                elif value.isdigit():
                    value = int(value)
                kwArgs[key] = value
            else:
                posArgs.append(arg)
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError, e:
            self.sendLine('Error: no such command.')
        else:
            try:
                method(*posArgs, **kwArgs)
            except Exception, e:
                self.sendLine('Error: ' + str(e))
        self.transport.write('> ')

    def do_help(self, command=None):
        if command:
            self.sendLine(getattr(self, 'do_' + command).__doc__)
        else:
            commands = [cmd[3:] for cmd in dir(self) if cmd.startswith('do_')]
            self.sendLine("Valid commands: " +" ".join(commands))

    def do_shutdown(self):
        self.sendLine('Shutting down.')
        reactor.stop()

    def do_agent(self, agentType, name):
        self.controller.createAgent(agentType, name)

    def do_job(self, jobType, agent, **kw):
        self.controller.enterJob(jobType, agent, params=kw)


class TelnetProtocol(CmdlineProtocol):

    delimiter = '\r\n'

    def do_quit(self):
        self.sendLine('Goodbye.')
        self.transport.loseConnection()


class TelnetServerFactory(protocol.ServerFactory):

    def __init__(self, controller):
        self.controller = controller

    def protocol(self, *args, **kw):
        prot = TelnetProtocol(*args, **kw)
        prot.controller = self.controller
        return prot

