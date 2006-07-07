# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass
from zope.interface import implements

from cybertools.brain.interfaces import INeuron, ISynapsis
from cybertools.brain.interfaces import IState, IStateTransformation, IStateMerger
from cybertools.brain.neuron import Neuron, Synapsis
from cybertools.brain.state import State, StateTransformation, StateMerger


class TestBrain(unittest.TestCase):
    "Basic tests for the brain package."

    def testInterfaces(self):
        pass


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestBrain),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
