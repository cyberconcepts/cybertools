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
State definition implementation.

$Id$
"""

from zope.interface import implements

from cybertools.stateful.interfaces import IStatesDefinition


class State(object):

    def __init__(self, id, title, transitions):
        self.id = id
        self.title = title
        self.transitions = transitions


class Transition(object):

    def __init__(self, id, title, targetState):
        self.id = id
        self.title = title
        self.targetState = targetState


class StatesDefinition(object):

    implements(IStatesDefinition)

    # Basic/example states definition:
    _states = {
        'started': State('started', 'Started', ('finish',)),
        'finished': State('finished', 'Finished', ()),
    }
    _transitions = {
        'finish': Transition('finish', 'Finish', 'finished')
    }
    _initialState = 'started'

    def doTransitionFor(self, object, transition):
        object._state = self._transitions[transition].targetState

    def getAvailableTransitionsFor(self, object):
        state = object.getState()
        return [ self._transitions[t] for t in self._states[state].transitions ]


statesDefinitions = {
    'default': StatesDefinition(),
}
