# $Id$

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing.functional import FunctionalDocFileSuite


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    browser = FunctionalDocFileSuite('skin/cyberview.txt', optionflags=flags)
    return unittest.TestSuite((browser,))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
