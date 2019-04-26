#! /usr/bin/python

"""
Tests for the 'cybertools.z2' package.
"""

import unittest, doctest

try:
    from Products.Five import BrowserView
    ignore = False
except ImportError:
    BrowserView = None
    ignore = True


class Test(unittest.TestCase):
    "Basic tests for the z2 package."

    def testBasicStuff(self):
        pass


def test_suite():
    if ignore:
        return unittest.TestSuite(())
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
