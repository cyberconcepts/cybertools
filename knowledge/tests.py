#! /usr/bin/python

"""
Tests for the 'cybertools.knowledge' package.
"""

import unittest, doctest
from cybertools.knowledge.knowing import Knowing

class TestKnowledge(unittest.TestCase):
    "Basic tests for the knowledge package."

    def testBasicStuff(self):
        p = Knowing()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestKnowledge),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
