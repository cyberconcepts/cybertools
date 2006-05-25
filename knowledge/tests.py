#! /usr/bin/python

"""
Tests for the 'cybertools.knowledge' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from cybertools.knowledge.knowing import Knowing

class TestKnowledge(unittest.TestCase):
    "Basic tests for the knowledge package."

    def testBasicStuff(self):
        p = Knowing()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestKnowledge),
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
