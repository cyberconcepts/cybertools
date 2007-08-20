#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
        """ Return the state (an IState implementation) of the object.
        """

    def doTransition(transition):
        """ Execute a transition; the transition is specified by its name.
        """

    def getAvailableTransitions():
        """ Return the transitions for this object that are available in
            the current state. The implementation of the returned transition
            objects is not specified, they may be action dictionaries or
            special Transition objects.
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

