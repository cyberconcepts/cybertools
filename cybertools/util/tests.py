# cybertools.util.tests

import unittest, doctest
import sys
import warnings
#print('***', sys.path)
sys.path = sys.path[1:]


class Test(unittest.TestCase):
    "Basic tests for modules in the util package."

    def testBasicStuff(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
        #doctest.DocTestSuite(cybertools.util.property, optionflags=flags),
        doctest.DocFileSuite('adapter.txt', optionflags=flags),
        #doctest.DocFileSuite('aop.txt', optionflags=flags),
        doctest.DocFileSuite('cache.txt', optionflags=flags),
        doctest.DocFileSuite('config.txt', optionflags=flags),
        doctest.DocFileSuite('defer.txt', optionflags=flags),
        doctest.DocFileSuite('format.txt', optionflags=flags),
        doctest.DocFileSuite('html.txt', optionflags=flags),
        doctest.DocFileSuite('iterate.txt', optionflags=flags),
        doctest.DocFileSuite('multikey.txt', optionflags=flags),
        doctest.DocFileSuite('property.txt', optionflags=flags),
        doctest.DocFileSuite('jeep.txt', optionflags=flags),
        doctest.DocFileSuite('randomname.txt', optionflags=flags),
        doctest.DocFileSuite('version.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
