# cybertools.brain.neuron

""" A simple basic implementation of Neuron and Synapsis.
"""

from zope.interface import implementer
from cybertools.brain.interfaces import INeuron, ISynapsis
from cybertools.brain.state import State, Transition


@implementer(ISynapsis)
class Synapsis(object):
    """ A synapsis connects two neurons.
    """

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


@implementer(INeuron)
class Neuron(object):

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

