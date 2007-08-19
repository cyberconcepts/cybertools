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
from zope.component import adapts
from zope.interface import implements

from cybertools.stateful.interfaces import IStateful
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

    def doTransition(self, transition):
        """ execute transition.
        """
        sd = self.getStatesDefinition()
        sd.doTransitionFor(self, transition)

    def getAvailableTransitions(self):
        sd = self.getStatesDefinition()
        return sd.getAvailableTransitionsFor(self)

    def getStatesDefinition(self):
        return statesDefinitions.get(self.statesDefinition, None)


class StatefulAdapter(Stateful):
    """ An adapter for persistent objects to make the stateful.
    """

    adapts(IPersistent)

    statesAttributeName = '__states__'

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

