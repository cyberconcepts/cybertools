
import unittest, doctest
import os
import warnings

testDir = os.path.join(os.path.dirname(__file__), 'testdata')

#warnings.filterwarnings('ignore', category=DeprecationWarning)


class Test(unittest.TestCase):
    "Basic tests for the loops.track package."

    def testBasics(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
        doctest.DocFileSuite('README.txt', optionflags=flags),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
