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
from cybertools.agent.components import agents, controllers, jobs
from cybertools.agent.components import loggers, schedulers
from cybertools.util.config import Configurator


class Agent(object):

    implements(IAgent)

    name = '???'
    master = None
    config = None
    logger = None

    def __init__(self, master):
        self.master = master
        self.config = master.config
        self.logger = master.logger

    def execute(self, job, params=None):
        pass

    def log(self, job, result='OK'):
        self.logger.log(dict(message='job execution', job=job.identifier,
                        agent=self.name, result=result))


class Master(Agent):

    name = 'master'
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
            if agent is None:
                print spec.type
                return
            agent.name = spec.name
            self.children[spec.name] = agent

    def setupJobs(self, jobSpecs):
        for spec in jobSpecs:
            job = jobs(self.scheduler, spec.type)
            job.agent = self.children[spec.agent]
            job.identifier = spec.identifier
            self.scheduler.schedule(job, spec.startTime)


class SampleAgent(Agent):

    def send(self, job):
        self.execute(job)

    def execute(self, job):
        print 'Job %s on agent %s has been executed.' % (job.identifier, self.name)
        self.log(job)

agents.register(SampleAgent, Master, name='base.sample')
