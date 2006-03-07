# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.interface import implements
from zope.app import zapi

from cybertools.typology.interfaces import IType, ITypeManager


class TestTypology(unittest.TestCase):
    "Basic tests for the typology package."

    def testInterfaces(self):
        pass


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestTypology),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
