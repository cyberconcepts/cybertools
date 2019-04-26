"""
unit tests, doc tests
"""

import unittest, doctest
from zope.interface.verify import verifyClass
from zope.interface import implements


class Test(unittest.TestCase):
    "Basic tests for the docgen package."

    def testInterfaces(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(Test),
                doctest.DocFileSuite('README.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
