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

    def stopThreads(self):
        reactor.threadpool.stop()

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
            DocFileSuite('crawl/filesystem.txt', optionflags=flags),
            DocFileSuite('crawl/outlook.txt', optionflags=flags),
            DocFileSuite('transport/transporter.txt', optionflags=flags),
            DocFileSuite('talk/README.txt', optionflags=flags),
    ))
    return testSuite


if __name__ == '__main__':
    standard_unittest.main(defaultTest='test_suite')
