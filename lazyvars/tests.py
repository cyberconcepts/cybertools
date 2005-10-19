# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import ztapi
from zope.app import zapi
from zope.interface.verify import verifyClass


class TestMenu(unittest.TestCase):
    "Test methods of the Menu class."

    
def test_suite():
    return unittest.TestSuite((
            DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
