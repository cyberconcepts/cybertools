# $Id$

import unittest
import doctest

import cybertools.util.property


class Test(unittest.TestCase):
    "Basic tests for modules in the util package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        #unittest.makeSuite(Test),  # we don't need this
        #doctest.DocTestSuite(cybertools.util.property, optionflags=flags),
        doctest.DocFileSuite('adapter.txt', optionflags=flags),
        doctest.DocFileSuite('aop.txt', optionflags=flags),
        doctest.DocFileSuite('cache.txt', optionflags=flags),
        doctest.DocFileSuite('config.txt', optionflags=flags),
        doctest.DocFileSuite('defer.txt', optionflags=flags),
        doctest.DocFileSuite('format.txt', optionflags=flags),
        doctest.DocFileSuite('html.txt', optionflags=flags),
        doctest.DocFileSuite('iterate.txt', optionflags=flags),
        doctest.DocFileSuite('multikey.txt', optionflags=flags),
        doctest.DocFileSuite('property.txt', optionflags=flags),
        doctest.DocFileSuite('json.txt', optionflags=flags),
        doctest.DocFileSuite('jeep.txt', optionflags=flags),
        doctest.DocFileSuite('randomname.txt', optionflags=flags),
        doctest.DocFileSuite('version.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
