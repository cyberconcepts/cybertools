# cybertools.reporter.tests

import unittest, doctest
from zope.app.testing import ztapi
from zope.interface.verify import verifyClass

from cybertools.reporter.interfaces import IResultSet, IRow, ICell


class Test(unittest.TestCase):
    "Basic tests for the reporter package."

    def testInterfaces(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
