#! /usr/bin/env python

# $Id$

import os, time
import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from twisted.internet import reactor
#from twisted.internet.defer import Deferred
#from twisted.trial import unittest as trial_unittest

baseDir = os.path.dirname(__file__)


class Tester(object):
    """ Used for controlled execution of reactor iteration cycles.
    """

    def iterate(self, n=10, delays={}):
        for i in range(n):
            delay = delays.get(i, 0)
            reactor.iterate(delay)

tester = Tester()


class Test(unittest.TestCase):
    "Basic tests for the cybertools.agent package."

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    testSuite = unittest.TestSuite((
            unittest.makeSuite(Test),
            DocFileSuite('README.txt', optionflags=flags),
            DocFileSuite('crawl/README.txt', optionflags=flags),
            DocFileSuite('crawl/Outlook.txt', optionflags=flags),
    ))
    return testSuite


if __name__ == '__main__':
    standard_unittest.main(defaultTest='test_suite')
