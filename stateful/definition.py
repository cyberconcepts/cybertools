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

from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import implements
from cybertools.util.jeep import Jeep

from cybertools.stateful.interfaces import IState, ITransition
from cybertools.stateful.interfaces import IStatesDefinition
from cybertools.stateful.interfaces import ITransitionEvent


class State(object):

    implements(IState)

    icon = None
    color = 'blue'

    def __init__(self, name, title, transitions, **kw):
        self.name = self.__name__ = name
        self.title = title
        self.transitions = transitions
        for k, v in kw.items():
            setattr(self, k, v)


class Transition(object):

    implements(ITransition)

    def __init__(self, name, title, targetState, **kw):
        self.name = self.__name__ = name
        self.title = title
        self.targetState = targetState
        for k, v in kw.items():
            setattr(self, k, v)


class StatesDefinition(object):

    implements(IStatesDefinition)

    initialState = 'started'

    def __init__(self, name, *details, **kw):
        self.name = self.__name__ = name
        self.states = Jeep()
        self.transitions = Jeep()
        for d in details:
            if ITransition.providedBy(d):
                self.transitions.append(d)
            elif IState.providedBy(d):
                self.states.append(d)
            else:
                raise TypeError('Only states or transitions are allowed here, '
                                'got %s instead.' % repr(d))
        for k, v in kw.items():
            setattr(self, k, v)

    def doTransitionFor(self, obj, transition):
        if transition not in self.transitions:
            raise ValueError('Transition %s is not available.' % transition)
        if transition not in [t.name for t in self.getAvailableTransitionsFor(obj)]:
            raise ValueError("Transition '%s' is not reachable from state '%s'."
                                    % (transition, obj.getState()))
        transObject = self.transitions[transition]
        previousState = obj.state
        obj.state = transObject.targetState
        notify(TransitionEvent(obj, transObject, previousState))

    def getAvailableTransitionsFor(self, obj):
        state = obj.getState()
        return [self.transitions[t] for t in self.states[state].transitions]


# event

class TransitionEvent(ObjectEvent):

    implements(ITransitionEvent)

    def __init__(self, obj, transition, previousState):
        super(TransitionEvent, self).__init__(obj)
        self.transition = transition
        self.previousState = previousState


# dummy default states definition

defaultSD = StatesDefinition('default',
    State('started', 'Started', ('finish',)),
    State('finished', 'Finished', ()),
    Transition('finish', 'Finish', 'finished'),
)


# states definitions registry

statesDefinitions = dict()

def registerStatesDefinition(definition):
    statesDefinitions[definition.name] = definition

registerStatesDefinition(defaultSD)
