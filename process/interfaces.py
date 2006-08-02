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

class IActivity(Interface):
    """ A step of a process - typically a state that lets the process wait
        for a user interaction or an action that is executed automatically.
    """

    successors = Attribute('A set of activities following this activity')
    handlerName = Attribute('Name of an adapter that may handle the '
                            'execution of this activity')
    qualifier = Attribute('A collection of strings giving additional '
                          'information about an activity. '
                          'May be used by an execution context '
                          'for deciding which activity it will execute next')

    def add(successor):
        """ Append an activity to the collection of following activities.
        """

    def execute(execution=None):
        """ Execute a activity in an execution context of a process instance;
            if this activity signifies a wait state this will create a work item.
            If the execution argument is None a new execution context will
            be created. The execution context is returned.
        """


class IProcess(Interface):
    """ The definition of a process or workflow.
    """

    startActivity = Attribute('The start activity of this process')

    def execute():
        """ Start the process (typically by executing its start activity).
            Return the execution context.
        """


class IActionHandler(Interface):
    """ Will be called for handling process executions. Is typically
        implemented as an adapter for IActivity.
    """

    def handle(execution):
        """ Handles the execution of a activity in the execution context given.
        """


# process execution


class IExecution(Interface):
    """ An execution context signifying the current state (or one of the
        current states) of a process instance.
    """

    currentActivity = Attribute('The activity this execution is currently in')
    workItem = Attribute('The work item the process instance is currently '
                         'waiting for; None if the current activity is not in a '
                         'waiting state')
    parent = Attribute('The execution context that has created this one '
                       'e.g. because of a forking operation')
    children = Attribute('A collection of execution contexts that have been '
                         'created by this one')

    def trigger(qualifiers=None):
        """ A callback (handler) that will may be called by an action handler.
            This will typically lead to moving on the execution context
            to a successor activity of the current activity. The execution
            context will use the qualifiers argument to decide which
            activities to transfer control to.
        """


class IWorkItem(Interface):
    """ A work item tells some external entity - typically a user - to
        do something in order to let the process proceed.
    """

    activity = Attribute('The activity this work item has been created from')
    execution = Attribute('The execution context that has created this work item')
    done = Attribute('A Boolean attribute that is true if the work '
                     'item has been submitted')

    def submit(data={}):
        """ Provide the work item with some data (optional) and have it
            continue the process by triggering the execution context.
            This should also set the `done` attribute to True.
        """
