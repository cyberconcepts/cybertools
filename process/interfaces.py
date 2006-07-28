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
Interfaces for process management.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zope')


# process/workflow definitions

class INode(Interface):
    """ A step of a process - typically a state that lets the process wait
        for a user interaction or an action that is executed automatically.
    """

    process = Attribute('The process this node belongs to')
    incoming = Attribute('Transitions that lead to this node')
    outgoing = Attribute('Transitions that lead to the next nodes')
    handlerName = Attribute('Name of an adapter that may handle the '
                            'execution of this node')

    def addTransition(destination):
        """ Append a transition to the destination node given
            to the collection of outgoing transitions.
        """

    def execute(execution):
        """ Execute a node in an execution context of a process instance;
            if this node signifies a wait state this will create a work item.
        """


class ITransition(Interface):
    """ A transition leading from one node (activity, state, action) to
        the next.
    """
    source = Attribute('The node that triggered this transition')
    destination = Attribute('The destination node of this transition')
    qualifier = Attribute('A string giving a hint for the meaning of the '
                          'transition. May be used by an execution context '
                          'for deciding which transition it will transfer '
                          'control to')

    def take(execution):
        """ Pass over the execution context from the source node to the
            destination node.
        """


class IProcessDefinition(Interface):
    """ The definition of a process or workflow.
    """

    instances = Attribute('A collection of process instances created from '
                          'this process definition')
    startNode = Attribute('The start node of this process')
    endNode = Attribute('The end node of this process')


class IActionHandler(Interface):
    """ Will be called for handling process executions. Is typically
        implemented as an adapter for INode.
    """

    def handle(execution):
        """ Handles the execution of a node in the execution context given.
        """

# process execution


class IExecution(Interface):
    """ An execution context signifying the current state (or one of the
        current states) of a process instance.
    """

    instance = Attribute('The process instance this execution context belongs to')
    currentNode = Attribute('The node the process instance is currently in')
    workItem = Attribute('The work item the process instance is currently '
                         'waiting for; None if the current node is not in a '
                         'waiting state')

    def trigger(transitionQualifiers=None):
        """ A callback (handler) that will may be called by an action handler.
            This will typically lead to moving on the execution context
            to an outgoing transition of the current node. The execution
            context will use the transitionQualifiers to decide which outgoing
            transition(s) to transfer control to.
        """


class IProcessInstance(Interface):
    """ An executing process, i.e. an execution context that keeps track of
        the currently active node(s) of the process.
    """

    process = Attribute('The process definition this instance is created from')
    executions = Attribute('A collection of currently active execution contexts')

    def execute():
        """ Start the execution of the process with its start node;
            return the execution context.
        """


class IWorkItem(Interface):
    """ An instance of an activity from a process definition.
    """

    node = Attribute('The node this work item has been created from')
    execution = Attribute('The execution context (and thus the process '
                          'instance) that has create this work item')


