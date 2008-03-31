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

from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.components import controllers
from cybertools.agent.interfaces import IController


class Controller(object):

    implements(IController)

    def __init__(self, agent):
        self.agent = agent

    def setupAgent(self):
        self.agent.setupAgents(self._getAgents())
        self.agent.setupJobs(self._getCurrentJobs())

    def _getAgents(self):
        return []

    def _getCurrentJobs(self):
        return []


class SampleController(Controller):

    jobNumber = 0

    agents = (('sample01', 'base.sample'),)

    def _getAgents(self):
        return [AgentSpecification(name, type) for name, type in self.agents]

    def createAgent(self, agentType, name):
        spec = AgentSpecification(name, agentType)
        self.agent.setupAgents([spec])

    def enterJob(self, jobType, agent):
        self.jobNumber += 1
        spec = JobSpecification(jobType, '%05i' % self.jobNumber, agent=agent)
        self.agent.setupJobs([spec])

controllers.register(SampleController, Master, name='base.sample')


class AgentSpecification(object):

    def __init__(self, name, type, **kw):
        self.name = name
        self.type = type
        for k, v in kw.items():
            setattr(self, k, v)


class JobSpecification(object):

    startTime = None

    def __init__(self, type, identifier, **kw):
        self.type = type
        self.identifier = identifier
        for k, v in kw.items():
            setattr(self, k, v)

