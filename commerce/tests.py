#! /usr/bin/python

"""
Tests for the 'cybertools.commerce' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from cybertools.commerce.product import Product

class Test(unittest.TestCase):
    "Basic tests."

    def testBasicStuff(self):
        p = Product()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
