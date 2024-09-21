# cybertools.brain.session

""" Transaction management.
"""

from zope.interface import implementer
from cybertools.brain.interfaces import ISession


implementer(ISession)
class Session(object):

    def __init__(self):
        self.states = {}

    def setState(self, neuron, state):
        self.states[neuron] = state

    def getState(self, neuron):
        return self.states.get(neuron, neuron.state)

