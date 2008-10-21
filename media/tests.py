#! /usr/bin/python

"""
Tests for the 'cybertools.media' package.

$Id$
"""

import os
import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.interface.verify import verifyClass

from cybertools import media

dataDir = os.path.join(os.path.dirname(media.__file__), 'testdata')

def clearDataDir():
    for fn in os.listdir(dataDir):
        path = os.path.join(dataDir, fn)
        if os.path.isdir(path):
            for subfn in os.listdir(path):
                os.unlink(os.path.join(path, subfn))
            os.rmdir(path)


class Test(unittest.TestCase):
    "Basic tests for the media package."

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
