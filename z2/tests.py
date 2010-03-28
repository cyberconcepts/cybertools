#! /usr/bin/python

"""
Tests for the 'cybertools.z2' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite

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
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
