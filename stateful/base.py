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

from cybertools.stateful.interfaces import IStateful
from cybertools.stateful.definition import statesDefinitions


class Stateful:

    implements(IStateful)

    _statesDefinition = 'default'
    _state = None

    def getState(self):
        if self._state is None:
            self._state = self.getStatesDefinition()._initialState
        return self._state

    def doTransition(self, transition):
        """ execute transition.
        """
        sd = self.getStatesDefinition()
        sd.doTransitionFor(self, transition)

    def getAvailableTransitions(self):
        sd = self.getStatesDefinition()
        return sd.getAvailableTransitionsFor(self)

    def getStatesDefinition(self):
        return statesDefinitions.get(self._statesDefinition, None)


