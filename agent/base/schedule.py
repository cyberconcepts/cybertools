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
Basic (sample) job scheduler.

$Id$
"""

from time import time
from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.components import schedulers
from cybertools.agent.interfaces import IScheduler


class Scheduler(object):

    implements(IScheduler)

    def __init__(self, agent):
        self.agent = agent
        self.queue = []

    def schedule(self, job, startTime=None):
        job.startTime = startTime or int(time())
        self.queue.append(job)
        job.execute()   # the sample scheduler does not care about startTime

    def getJobsToExecute(startTime=0):
        return [j for j in self.queue.values() if startTime <= j.startTime]


schedulers.register(Scheduler, Master, name='sample')
#schedulers.register(Scheduler, Master, name='BasicCrawler')
