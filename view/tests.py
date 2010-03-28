#! /usr/bin/python

"""
Tests for the 'cybertools.index' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite

from cybertools.view.pac import View


class Test(unittest.TestCase):
    "Basic tests for the index package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                DocFileSuite('README.txt', optionflags=flags),
                unittest.makeSuite(Test),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
