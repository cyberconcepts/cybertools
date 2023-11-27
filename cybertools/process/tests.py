#! /usr/bin/python

"""
Tests for the 'cybertools.process' package.
"""

import unittest, doctest
from cybertools.process.definition import Process

class TestProcess(unittest.TestCase):
    "Basic tests for the process package."

    def testBasicStuff(self):
        p = Process()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestProcess),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
