#! /usr/bin/python

"""
Tests for the 'cybertools.text' package.
"""
import sys
#sys.path = [p for p in sys.path if p != '']
sys.path = sys.path[2:] # avoid import cycle with bs4 when importing html
#print(sys.path)

import unittest, doctest
import warnings
from cybertools.text import pdf
from cybertools.text.html import htmlToText



class Test(unittest.TestCase):
    "Basic tests for the text package."

    def testBasicStuff(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
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
