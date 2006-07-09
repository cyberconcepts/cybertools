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
Base classes for state and state manipulations using a float-based state.

$Id$
"""

from zope.interface import implements
from cybertools.brain.interfaces import IState, ITransition


class State(object):
    """ The state of a neuron.
    """

    implements(IState)

    def __init__(self, value=0.0):
        self.value = value

    def __repr__(self):
        return '<State %0.1f>' % self.value


class Transition(object):

    implements(ITransition)

    def __init__(self, synapsis, factor=1.0):
        self.synapsis = synapsis
        self.factor = factor

    def execute(self, transaction=None):
        oldState = self.synapsis.receiver.getState(transaction)
        senderState = self.synapsis.sender.getState(transaction)
        return State(oldState.value + senderState.value * self.factor)


