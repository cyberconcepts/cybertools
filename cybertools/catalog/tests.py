#! /usr/bin/python

"""
Tests for the 'cybertools.catalog' package.
"""

import unittest, doctest


class Test(unittest.TestCase):
    "Basic tests for the cybertools.catalog package."

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
