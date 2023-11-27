#! /usr/bin/python

"""
Tests for the 'cybertools.roa' (Resource-oriented Architecture) package.
"""

import unittest, doctest
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
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
