#! /usr/bin/python

"""
Tests for the 'cybertools.storage' package.
"""

import unittest, doctest
from cybertools.text import pdf

class Test(unittest.TestCase):
    "Basic tests for the storage package."

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
