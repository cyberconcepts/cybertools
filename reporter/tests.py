# $Id$

import unittest
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
    return unittest.TestSuite((
                unittest.makeSuite(TestReporter),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
