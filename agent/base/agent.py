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
from cybertools.agent.components import agents
from cybertools.agent.components import controllers, loggers, schedulers
from cybertools.util.config import Configurator


class Agent(object):

    implements(IAgent)

    master = None
    config = None
    logger = None

    def __init__(self, master):
        self.master = master
        self.config = master.config
        self.logger = master.logger

    def execute(self, job, params=None):
        pass


class Master(Agent):

    scheduler = None

    def __init__(self, configuration=None):
        config = self.config = Configurator()
        self.master = self
        self.controllers = []
        self.children = {}
        if configuration is not None:
            config.load(configuration)
            self.logger = loggers(self, name=config.logger.name)
            self.controllers.append(controllers(self, name=config.controller.name))
            self.scheduler = schedulers(self, name=config.scheduler.name)

    def setup(self):
        for cont in self.controllers:
            cont.setupAgent()

    def setupAgents(self, agentSpecs):
        for spec in agentSpecs:
            agent = agents(self, spec.type)
            self.children[spec.name] = agent

    def setupJobs(self, jobSpecs):
        pass


class SampleAgent(Agent):

    pass

agents.register(SampleAgent, Master, name='sample')

