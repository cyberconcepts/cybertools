# $Id$

import unittest
import doctest
from twisted.internet import reactor

import cybertools.twisted.deferring


class Tester(object):

    def iterate(self, n=10, delays={}):
        for i in range(n):
            delay = delays.get(i, 0)
            reactor.iterate(delay)

tester = Tester()


class Test(unittest.TestCase):
    "Basic tests for modules in the util package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        #unittest.makeSuite(Test),  # we don't need this
        #doctest.DocTestSuite(cybertools.util.property, optionflags=flags),
        doctest.DocFileSuite('deferring.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
