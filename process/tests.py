#! /usr/bin/python

"""
Tests for the 'cybertools.process' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from cybertools.process.definition import ProcessDefinition

class TestProcess(unittest.TestCase):
    "Basic tests for the process package."

    def testBasicStuff(self):
        p = ProcessDefinition()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestProcess),
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
