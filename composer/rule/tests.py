# $Id$

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite

from cybertools.composer.rule.base import ActionHandler


class MailActionHandler(ActionHandler):

    def __call__(self, data, event, params={}):
        pass


class Test(unittest.TestCase):
    "Basic tests."

    def testBasics(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(Test),
                DocFileSuite('README.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
