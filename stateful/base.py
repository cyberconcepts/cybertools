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
Basic implementations for stateful objects and adapters.

$Id$
"""

from persistent.interfaces import IPersistent
from persistent.mapping import PersistentMapping
from zope import component
from zope.component import adapts
from zope.interface import implements

from cybertools.stateful.interfaces import IStateful, IStatefulIndexInfo
from cybertools.stateful.definition import statesDefinitions


class Stateful(object):

    implements(IStateful)

    statesDefinition = 'default'
    state = None

    def getState(self):
        if self.state is None:
            self.state = self.getStatesDefinition().initialState
        return self.state

    def getStateObject(self):
        state = self.getState()
        return self.getStatesDefinition().states[state]

    def doTransition(self, transition, historyInfo=None):
        sd = self.getStatesDefinition()
        if isinstance(transition, basestring):
            sd.doTransitionFor(self, transition)
            return
        available = [t.name for t in sd.getAvailableTransitionsFor(self)]
        for tr in transition:
            if tr in available:
                sd.doTransitionFor(self, tr)
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


class StatefulAdapter(Stateful):
    """ An adapter for persistent objects to make them stateful.
    """

    adapts(IPersistent)

    statesAttributeName = '__stateful_states__'

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

