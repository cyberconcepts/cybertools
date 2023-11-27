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
A simple basic implementation of Neuron and Synapsis.

$Id$
"""

from zope.interface import implements
from cybertools.brain.interfaces import INeuron, ISynapsis
from cybertools.brain.state import State, Transition


class Synapsis(object):
    """ A synapsis connects two neurons.
    """

    implements(ISynapsis)

    def __init__(self, sender, receiver):
        self.sender = sender
        sender.receivers.append(self)
        self.receiver = receiver
        receiver.senders.append(self)
        self.transition = Transition(self)

    def trigger(self, session=None):
        receiver = self.receiver
        receiver.setState(self.transition.execute(session), session)
        receiver.notify(session)


class Neuron(object):

    implements(INeuron)

    def __init__(self):
        self.senders = []
        self.receivers = []
        self.state = State()

    def setState(self, state, session=None):
        if session is None:
            self.state = state
        else:
            session.setState(self, state)

    def getState(self, session=None):
        if session is None:
                return self.state
        return session.getState(self)

    def notify(self, session=None):
        for r in self.receivers:
            r.trigger(session)

