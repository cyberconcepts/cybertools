#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Execution of a process.

$Id$
"""

from zope.interface import implements
from zope.component import adapts
from cybertools.process.interfaces import IActivity, IExecution
from cybertools.process.interfaces import IWorkItem, IActionHandler


class Execution(object):

    implements(IExecution)

    def __init__(self, parent=None):
        self._currentActivity = None
        self._workItem = None
        self._parent = parent
        self._children = set()

    def getCurrentActivity(self): return self._currentActivity
    def setCurrentActivity(self, activity): self._currentActivity = activity
    currentActivity = property(getCurrentActivity, setCurrentActivity)

    def getWorkItem(self): return self._workItem
    def setWorkItem(self, item): self._workItem = item
    workItem = property(getWorkItem, setWorkItem)

    @property
    def parent(self): return self._parent

    @property
    def children(self): return self._children

    def trigger(self, qualifiers=set()):
        successors = [s for s in self.currentActivity.successors
                        if not qualifiers
                            or qualifiers.union(successor.qualifiers)]
        for successor in successors:
            if len(successors) == 1:
                execution = self
            else:
                execution = Execution(self)
                self.children.add(execution)
            successor.execute(execution)


class WorkItem(object):

    implements(IWorkItem)

    def __init__(self, execution):
        self._execution = execution
        self._activity = execution.currentActivity

    @property
    def execution(self): return self._execution

    @property
    def activity(self): return self._activity

    _done = False
    @property
    def done(self): return self._done

    def submit(self, data={}):
        _done = True
        self.execution.trigger()


class WorkActionHandler(object):
    """ A simple action handler that creates a work item.
    """

    implements(IActionHandler)
    adapts(IActivity)

    def __init__(self, context):
        self.context = context

    def handle(self, execution):
        self.workItem = WorkItem(execution)

