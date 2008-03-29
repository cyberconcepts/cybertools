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
Queueable agent base/sample classes.

$Id$
"""

from twisted.internet.defer import succeed
from zope.interface import implements

from cybertools.agent.base.agent import Agent, Master
from cybertools.agent.components import agents
from cybertools.agent.interfaces import IQueueableAgent


class QueueableAgent(Agent):

    implements(IQueueableAgent)

    currentJob = None

    def __init__(self, master):
        super(QueueableAgent, self).__init__(master)
        self.queue = []

    def send(self, job):
        if self.currentJob is None:
            if self.queue:  # this should not happen...
                self.queue.insert(0, job)
                job = self.queue.pop()
            self.execute(job)
        else:
            self.queue.insert(0, job)

    def execute(self, job):
        self.currentJob = job
        d = self.process()
        d.addCallbacks(self.completed, self.error)

    def process(self):
        # do something with the current job, return a deferred
        print ('Job %s on agent %s has been executed.'
            % (self.currentJob.identifier, self.name))
        return succeed('Done')

    def completed(self, result):
        self.log(self.currentJob)
        # TODO: inform the master about the result of the job execution
        self.finishJob()

    def error(self, result):
        print '*** error', result
        self.log(self.currentJob, result='Error')
        # TODO: inform the master about the result of the job execution
        self.finishJob()

    def finishJob(self):
        self.currentJob = None
        if self.queue:
            job = self.queue.pop()
            self.execute(job, job.params)

agents.register(QueueableAgent, Master, name='core.sample')
