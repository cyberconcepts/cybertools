
import unittest, doctest

import cybertools.zutil.jeep


class Test(unittest.TestCase):
    "Basic tests for modules in the util package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        #unittest.makeSuite(Test),  # we don't need this
        #doctest.DocTestSuite(cybertools.zutil.property, optionflags=flags),
        doctest.DocFileSuite('jeep.txt', optionflags=flags),
        doctest.DocFileSuite('rcache.txt', optionflags=flags),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
