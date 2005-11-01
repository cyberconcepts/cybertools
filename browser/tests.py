# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass
from zope.app import zapi


def test_suite():
    return unittest.TestSuite((
                unittest.makeSuite(TestMenu),
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
