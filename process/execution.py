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
from cybertools.process.interfaces import IExecution, IProcessInstance


class Execution(object):

    implements(IExecution)

    def __init__(self, instance):
        self._instance = instance
        self._currentNode = None
        self._workItem = None

    @property
    def instance(self): return self._instance

    def getCurrentNode(self): return self._currentNode
    def setCurrentNode(self, node): self._currentNode = node
    currentNode = property(getCurrentNode, setCurrentNode)

    def getWorkItem(self): return self._workItem
    def setWorkItem(self, item): self._workItem = item
    workItem = property(getWorkItem, setWorkItem)

    def trigger(self, transitionPattern=None):
        outgoing = self.currentNode.outgoing
        if outgoing:
            transition = iter(outgoing).next()
            transition.take(self)


class ProcessInstance(object):

    implements(IProcessInstance)

    def __init__(self, process):
        self._process = process
        self._executions = set()

    @property
    def process(self): return self._process

    @property
    def executions(self): return self._executions

    def execute(self):
        execution = Execution(self)
        self.executions.add(execution)
        self.process.startNode.execute(execution)
        return execution
