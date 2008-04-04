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

import os
from twisted.internet import reactor

from cybertools.agent.base.agent import Master


application = None  # contains application object if started via twistd


def getConfig():
    agentHome = os.path.abspath(os.path.dirname(__file__))
    configName = 'agent.cfg'
    configFile = open(os.path.join(agentHome, configName))
    config = configFile.read()
    configFile.close()
    return config


def setup():
    master = Master(getConfig())
    master.setup()
    print 'Starting agent application...'
    print 'Using controllers %s.' % ', '.join(master.config.controller.names)


def startReactor():
    reactor.run()
    print 'Agent application has been stopped.'


if __name__ == '__main__':
    setup()
    startReactor()
