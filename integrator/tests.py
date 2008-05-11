# $Id$

import os
import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass


baseDir = os.path.dirname(__file__)
testDir = os.path.join(baseDir, 'testing', 'data')


class Test(unittest.TestCase):
    "Basic tests for the cybertools.integrator package."

    def testSomething(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(Test),
                DocFileSuite('README.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
