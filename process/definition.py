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
Process definitions.

$Id$
"""

from zope import component
from zope.interface import implements
from cybertools.process.interfaces import INode, ITransition, IProcessDefinition
from cybertools.process.interfaces import IActionHandler


class Node(object):

    implements(INode)

    def __init__(self, process=None, name=u'', title=u'', handlerName=''):
        self._process = process
        self._incoming = set()
        self._outgoing = set()
        self._handlerName = handlerName
        self.__name__ = name
        self.title = title

    def getProcess(self): return self._process
    def setProcess(self, prc): self._process = prc
    process = property(getProcess, setProcess)

    @property
    def outgoing(self): return self._outgoing

    @property
    def incoming(self): return self._incoming

    def getHandlerName(self): return self._handlerName
    def setHandlerName(self, name): self._handlerName = name
    handlerName = property(getHandlerName, setHandlerName)

    def addTransition(self, destination):
        transition = Transition(destination)
        self.outgoing.add(transition)
        transition.source = self
        if transition.destination.process is None:
            transition.destination.process = self.process

    def execute(self, execution):
        execution.currentNode = self
        handler = component.queryAdapter(self, IActionHandler, name=self.handlerName)
        if handler is not None:
            handler.handle(execution) # creates work item; work item triggers execution
        else:
            execution.trigger()


class Transition(object):

    implements(ITransition)

    def __init__(self, destination, qualifier=u''):
        self._source = None
        self._destination = destination
        self._qualifier = qualifier

    def getSource(self): return self._source
    def setSource(self, node): self._source = node
    source = property(getSource, setSource)

    def getDestination(self): return self._destination
    def setDestination(self, node): self._destination = node
    destination = property(getDestination, setDestination)

    def getQualifier(self): return self._qualifier
    def setQualifier(self, node): self._qualifier = node
    qualifier = property(getQualifier, setQualifier)

    def take(self, execution):
        self.destination.execute(execution)


class ProcessDefinition(object):

    implements(IProcessDefinition)

    def __init__(self):
        self._instances = set()
        self._startNode = Node(self)
        self._endNode = Node(self)

    @property
    def instances(self): return self._instances

    def getStartNode(self): return self._startNode
    def setStartNode(self, node): self._startNode = node
    startNode = property(getStartNode, setStartNode)

    def getEndNode(self): return self._endNode
    def setEndNode(self, node): self._endNode = node
    endNode = property(getEndNode, setEndNode)
