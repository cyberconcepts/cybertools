# $Id$

import os
import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass


baseDir = os.path.dirname(os.path.dirname(__file__))
testDir = os.path.join(baseDir, 'tests', 'data')

flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


class Test(unittest.TestCase):
    "Basic tests for the cybertools.integrator package."

    def testSomething(self):
        pass


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(Test),
                DocFileSuite('../filesystem.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
