# $Id$

import unittest
from zope.testing.doctestunit import DocFileSuite


def test_suite():
    return unittest.TestSuite((
                DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
