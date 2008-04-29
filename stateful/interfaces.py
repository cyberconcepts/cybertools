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
Interfaces for the `stateful` package.

$Id$
"""

try:
    from zope.component.interfaces import IObjectEvent
except ImportError: # Zope 2.9
    from zope.app.event.interfaces import IObjectEvent
from zope.interface import Interface, Attribute


class IState(Interface):

    name = Attribute('The name or identifier of the state')
    title = Attribute('A user-readable name or title of the state')
    transitions = Attribute('A sequence of strings naming the transitions '
                    'that can be executed from this state')


class ITransition(Interface):

    name = Attribute('The name or identifier of the transition')
    title = Attribute('A user-readable name or title of the transition')
    targetState = Attribute('A string naming the state that will be the '
                    'result of executing this transition')


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


class IStatefulIndexInfo(Interface):
    """ Provide a list of tokens to be used for index the states
        of an object in the catalog.
    """

    tokens = Attribute('A sequence of strings to be used for indexing the '
                'states; format: [<statesdefinition name>:<state name>, ...].')

    availableStatesDefinitions = Attribute('A sequence of strings with the '
                'names of all states definitions currently available.')


class ITransitionEvent(IObjectEvent):
    """ Fires when the state of an object is changed.
    """

    transition = Attribute('The transition.')
    previousState = Attribute('The name of the state before the transition.')
