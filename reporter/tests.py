# $Id$

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.interface import implements
from zope.app import zapi

from cybertools.reporter.interfaces import IResultSet, IRow, ICell


class TestReporter(unittest.TestCase):
    "Basic tests for the reporter package."

    def testInterfaces(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(TestReporter),
                DocFileSuite('README.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
