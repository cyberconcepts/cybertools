#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
Interfaces for the `stateful` package.
"""

try:
    from zope.component.interfaces import IObjectEvent
except ImportError: # Zope 2.9
    from zope.app.event.interfaces import IObjectEvent
from zope.interface import Interface, Attribute


class IState(Interface):

    name = Attribute('The name or identifier of the state')
    title = Attribute('A user-readable name or title of the state')
    transitions = Attribute('A collection of strings naming the transitions '
                    'that can be executed from this state.')
    actions = Attribute('A mapping with actions that may be executed in '
                    'this state.')
    setSecurity = Attribute('A callable (argument: stateful object) '
                    'for setting the security settings on the object.')


class IAction(Interface):

    name = Attribute('The name or identifier of the action.')
    title = Attribute('A user-readable name or title of the action.')
    allowed = Attribute('A boolean; if False the action may not be executed.')
    doBefore = Attribute('A callable (argument: stateful object) to be executed '
                    'before this action.')
    roles = Attribute('A collection of names of the roles that are allowed '
                    'to execute this action; no check when empty.')
    permission = Attribute('The name of a permission that is needed for '
                    'executing this action; no check when empty.')
    actors = Attribute('A collection of names of actors or groups that should be '
                    'able to execute this action; no check when empty. '
                    'See the IStateful.getActors().')
    condition = Attribute('A boolean function with a stateful object as '
                    'parameter. The action is only allowed if return value '
                    'is True. No check when condition is None.')
    schema = Attribute('An optional schema (a sequence of field specifications) '
                    'that provides information on fields to be shown in a '
                    'form used for executing the action.')


class ITransition(IAction):

    targetState = Attribute('A string naming the state that will be the '
                    'result of executing this transition.')


class IStateful(Interface):
    """ Provides basic methods for stateful objects.
    """

    def getState():
        """ Return the name of the state of the object.
        """

    def getStateObject():
        """ Return the state (an IState implementation) of the context object.
        """

    def doTransition(transition, historyInfo=None):
        """ Execute a transition; the transition is specified by its name.

            The ``transition`` argument may be an iterable; in this case
            its elements will be checked against the available transitions
            and the first one that's available will be executed.

            The ``historyInfo`` argument is an arbitrary object that will be
            used for recording the transition execution in the history
            (only if the context object is adaptable to IHistorizable).
        """

    def getAvailableTransitions():
        """ Return the transitions for this object that are available in
            the current state. The returned transition objects should
            provide the ITransition interface.
        """

    def getAvailableTransitionsForUser():
        """ Return the transitions for this object that are available for
            the current user. This is a subset of all available transitions
            for the current state.
        """

    def getActors():
        """ Return a collection of names of actors or groups that will be
            used for checking if a certain transition is allowed. May be 
            None in which case not checking should be applied.
        """

    def notify(transition, previousState):
        """ This method will be called upon completion of a transition.
        """


    request = Attribute('Optional publication request.')


class IHistorizable(Interface):
    """ An object that may record history information, e.g. when
        performing a state transition.
    """

    def record(info):
        """ Record the information given (typically a mapping) with the
            object.
        """

    def recordTransition(stateFrom, stateTo, transition, historyInfo=None):
        """ Record the state transition characterized by the arguments
            (names of the states and the transition), optionally
            supplemented by the additional history information given.
        """


class IStatesDefinition(Interface):
    """ A simple definition for a set of states and transitions between them,
        Similar to an entity-based workflow definition.
    """

    name = Attribute('The name or identifier of the states definition')

    def doTransitionFor(object, transition):
        """ Execute a transition for the object given;
            the transition is specified by its name.
        """

    def getAvailableTransitionsFor(object):
        """ Return the transitions available for this object in its current state.
        """

    def isAllowed(action, object):
        """ Return True if the action (an IAction provider) is allowed on
            the object given for the current user.
        """

    def checkRoles(roles, object):
        """ Return True if the current user provides one of the roles given
            on the object given.
        """

    def checkRoles(permission, object):
        """ Return True if the current user has the permission given
            on the object given.
        """


class IStatefulIndexInfo(Interface):
    """ Provide a list of tokens to be used for indexing the states
        of an object in the catalog.
    """

    tokens = Attribute('A sequence of strings to be used for indexing the '
                'states; format: [<statesdefinition name>:<state name>, ...].')

    availableStatesDefinitions = Attribute('A sequence of strings with the '
                'names of all states definitions currently available.')


class ITransitionEvent(IObjectEvent):
    """ Fires when the state of an object has been changed.
    """

    transition = Attribute('The transition.')
    previousState = Attribute('The name of the state before the transition.')
    request = Attribute('Optional publication request.')
