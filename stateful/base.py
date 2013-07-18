#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Basic implementations for stateful objects and adapters.

$Id$
"""

from persistent.interfaces import IPersistent
from persistent.mapping import PersistentMapping
from zope import component
from zope.component import adapts
try:
    from zope.component.interfaces import ObjectEvent
except ImportError: # Zope 2.9
    from zope.app.event.objectevent import ObjectEvent
from zope.event import notify
from zope.interface import implements

from cybertools.stateful.definition import statesDefinitions
from cybertools.stateful.interfaces import IStateful, IStatefulIndexInfo
from cybertools.stateful.interfaces import ITransitionEvent


class Stateful(object):

    implements(IStateful)

    statesDefinition = 'default'
    state = None

    def getState(self):
        if self.state is None:
            self.state = self.getStatesDefinition().initialState
        return self.state

    def getStateObject(self):
        states = self.getStatesDefinition().states
        if self.state not in states:
            self.state = self.getStatesDefinition().initialState
        return states[self.state]

    def doTransition(self, transition, historyInfo=None):
        sd = self.getStatesDefinition()
        previousState = self.getState()
        if isinstance(transition, basestring):
            sd.doTransitionFor(self, transition)
            self.notify(transition, previousState)
            return
        available = [t.name for t in sd.getAvailableTransitionsFor(self)]
        for tr in transition:
            if tr in available:
                sd.doTransitionFor(self, tr)
                self.notify(tr, previousState)
                return
        raise ValueError("None of the transitions '%s' is available for state '%s'."
                                % (repr(transition), self.getState()))

    def getAvailableTransitions(self):
        sd = self.getStatesDefinition()
        return sd.getAvailableTransitionsFor(self)

    def getAvailableTransitionsForUser(self):
        return self.getAvailableTransitions()

    def getStatesDefinition(self):
        return statesDefinitions.get(self.statesDefinition, None)

    def getActors(self):
        return None

    def notify(self, transition, previousState):
        """ To be implemented by subclass.
        """


class StatefulAdapter(Stateful):
    """ An adapter for persistent objects to make them stateful.
    """

    adapts(IPersistent)

    statesAttributeName = '__stateful_states__'

    request = None

    def __init__(self, context):
        self.context = context

    def getState(self):
        statesAttr = getattr(self.context, self.statesAttributeName, {})
        return statesAttr.get(self.statesDefinition,
                              self.getStatesDefinition().initialState)
    def setState(self, value):
        statesAttr = getattr(self.context, self.statesAttributeName, None)
        if statesAttr is None:
            statesAttr = PersistentMapping()
            setattr(self.context, self.statesAttributeName, statesAttr)
        statesAttr[self.statesDefinition] = value
    state = property(getState, setState)

    def notify(self, transition, previousState):
        transObject = self.getStatesDefinition().transitions[transition]
        notify(TransitionEvent(self.context, transObject, previousState, self.request))


class IndexInfo(object):

    implements(IStatefulIndexInfo)

    availableStatesDefinitions = []     # to be overwritten by subclass!

    def __init__(self, context):
        self.context = context

    @property
    def tokens(self):
        for std in self.availableStatesDefinitions:
            stf = component.getAdapter(self.context, IStateful, name=std)
            yield ':'.join((std, stf.state))


# event

class TransitionEvent(ObjectEvent):

    implements(ITransitionEvent)

    def __init__(self, obj, transition, previousState, request=None):
        super(TransitionEvent, self).__init__(obj)
        self.transition = transition
        self.previousState = previousState
        self.request = request
