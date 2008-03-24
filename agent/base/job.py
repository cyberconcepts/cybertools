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
The real agent stuff.

$Id$
"""

from zope.interface import implements

from cybertools.agent.base.schedule import Scheduler
from cybertools.agent.components import jobs
from cybertools.agent.interfaces import IScheduledJob


class Job(object):

    implements(IScheduledJob)

    identifier = '???'
    agent = None
    startTime = None
    repeat = 0
    whenStarted = whenFinished = None

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.params = {}
        self.successors = []

    def execute(self):
        if self.agent is not None:
            self.agent.execute(self, self.params)

    def reschedule(self, startTime=None):
        self.scheduler.schedule(self.copy(), startTime)

    def copy(self):
        newJob = Job(self.scheduler)
        newJob.agent = self.agent
        newJob.params = self.params
        newJob.repeat = self.repeat
        newJob.successors = [s.copy() for s in self.successors]

jobs.register(Job, Scheduler, name='sample')
