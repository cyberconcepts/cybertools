# cybertools.util.docgen.tests

""" unit tests, doc tests
"""

import unittest, doctest
import warnings
from zope.interface.verify import verifyClass


class Test(unittest.TestCase):
    "Basic tests for the docgen package."

    def testInterfaces(self):
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
