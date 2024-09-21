#! /usr/bin/python

"""
Tests for the 'cybertools.text' package.
"""
import sys
#sys.path = [p for p in sys.path if p != '']
sys.path = sys.path[2:]
print(sys.path)

import unittest, doctest
import warnings
from cybertools.text import pdf
from cybertools.text.html import htmlToText

warnings.filterwarnings('ignore', category=ResourceWarning)


class Test(unittest.TestCase):
    "Basic tests for the text package."

    def testBasicStuff(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(Test),
        doctest.DocFileSuite('README.txt', optionflags=flags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
