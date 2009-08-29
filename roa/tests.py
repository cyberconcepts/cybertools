#! /usr/bin/python

"""
Tests for the 'cybertools.roa' (Resource-oriented Architecture) package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope import component
from cybertools.roa import json


class Test(unittest.TestCase):
    "Basic tests for the rest package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
