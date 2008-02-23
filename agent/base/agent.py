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
Agent base and sample classes.

$Id$
"""

from zope.interface import implements

from cybertools.agent.interfaces import IAgent
from cybertools.util.config import Configurator


class Agent(object):

    implements(IAgent)

    master = None
    logger = None

    def execute(self, job, params=None):
        pass


class Master(Agent):

    config = None
    controller = None
    scheduler = None

    def __init__(self, configuration=None):
        self.config = Configurator()
        if configuration is not None:
            self.config.load(configuration)

    def setup(self):
        pass


class SampleAgent(Agent):

    pass

