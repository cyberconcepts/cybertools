
import unittest, doctest
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)


class Test(unittest.TestCase):
    "Basic tests for the cybertools.tracking.notify package."

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
