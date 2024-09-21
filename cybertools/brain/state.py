# cybertools.brain.state

""" Base classes for state and state manipulations using a float-based state.
"""

from zope.interface import implementer
from cybertools.brain.interfaces import IState, ITransition


@implementer(IState)
class State(object):
    """ The state of a neuron.
    """

    def __init__(self, value=0.0):
        self.value = value

    def __repr__(self):
        return '<State %0.1f>' % self.value


@implementer(ITransition)
class Transition(object):

    def __init__(self, synapsis, factor=1.0):
        self.synapsis = synapsis
        self.factor = factor

    def execute(self, session=None):
        oldState = self.synapsis.receiver.getState(session)
        senderState = self.synapsis.sender.getState(session)
        return State(oldState.value + senderState.value * self.factor)


