# $Id$

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass

from cybertools.brain.interfaces import INeuron, ISynapsis
from cybertools.brain.interfaces import IState, ITransition
from cybertools.brain.neuron import Neuron, Synapsis
from cybertools.brain.state import State, Transition


class TestBrain(unittest.TestCase):
    "Basic tests for the brain package."

    def testInterfaces(self):
        verifyClass(INeuron, Neuron)


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(TestBrain),
                DocFileSuite('README.txt',
                             optionflags=flags,),
           ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
