#! /usr/bin/env python2.4
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
Agent application.

$Id$
"""

import sys
import os
from twisted.internet import reactor

from cybertools.agent.base.agent import Master
from cybertools.agent.crawl.base import Metadata, Resource


application = None  # contains application object if started via twistd


def getConfig():
    agentHome = os.path.abspath(os.path.dirname(__file__))
    configName = 'transporter.cfg'
    configFile = open(os.path.join(agentHome, configName))
    config = configFile.read()
    configFile.close()
    return config


def setup(configInfo=None):
    if configInfo is None:
        configInfo = getConfig()
    master = Master(configInfo)
    setupEnvironment(master.config)
    master.setup()
    print 'Starting agent application...'
    print 'Using controllers %s.' % ', '.join(master.config.controller.names)
    return master


def setupEnvironment(config):
    from cybertools.agent.base import agent, control, job, log, schedule
    from cybertools.agent.core import agent, control, schedule
    from cybertools.agent.control import cmdline
    from cybertools.agent.system import rpcapi
    rpcapi.setup(config)
    from cybertools.agent.system import sftpapi
    sftpapi.setup(config)
    from cybertools.agent.transport import remote


def startReactor():
    reactor.run()
    print 'Agent application has been stopped.'


if __name__ == '__main__':
    master = setup()
    controller = master.controllers[0]
    controller.createAgent('transport.remote', 'sample03')
    metadata01 = Metadata(dict(filename='dummy.txt'))
    res01 = Resource()
    res01.metadata = metadata01
    res01.path = 'data/file1.txt'
    controller.enterJob('sample', 'sample03', params=dict(resource=res01))
    startReactor()
