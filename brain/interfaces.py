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
Interfaces for a sort of neural network.

$Id$
"""

from zope.interface import Interface, Attribute


class ISynapsis(Interface):
    """ A synapsis connects two neurons.
    """

    sender = Attribute("The sender neuron for this synapsis")
    reciever = Attribute("The receiver neuron for this synapsis")

    transition = Attribute("A transition changes the sender neuron's state.")

    def trigger(session=None):
        """ Recalculate the receiver neuron's state by executing the
            synapse's transition using the state of the sender neuron.
        """


class INeuron(Interface):

    senders = Attribute("The sender synapses")
    receivers = Attribute("The receiver synapses")

    def setState(state, session=None):
        """ Set the neuron's state.
        """

    def getState(session=None):
        """ Return the neuron's state.
        """

    def notify(session=None):
        """ Notifies the neuron that something has happened. This method
            calls the trigger() method on all downstream (receiver) synapses.
            In addition it may perform side effects like changing
            transition properties of adjacent synapses or even create new
            synapses or neurons; this side effects should happen before
            triggering the receiver synapses.
        """


class IState(Interface):
    """ The state of a neuron.
    """


class ITransition(Interface):

    def execute(session=None):
        """ Transform the receiver's state to a new state value and return it.
        """


class ISession(Interface):
    """ A session keeps all actions for a certain sequence of user interactions
        together by keeping track of the neurons' current and cumulated states.
    """

