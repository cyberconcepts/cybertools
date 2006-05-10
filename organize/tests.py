#! /usr/bin/python

"""
Tests for the 'cybertools.organize' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from cybertools.organize.party import Person

class TestParty(unittest.TestCase):
    "Basic tests for the party module."

    def testBasicStuff(self):
        p = Person('Meier', 'Hans')
        self.assertEqual('Hans', p.firstName)
        self.assertEqual('Meier', p.lastName)


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(TestParty),
        DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
