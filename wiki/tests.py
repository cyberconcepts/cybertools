#! /usr/bin/python

"""
Tests for the 'cybertools.wiki' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope import component

from cybertools.wiki.base.config import WikiConfiguration
from cybertools.wiki.base.process import TreeProcessor
from cybertools.wiki.base.link import LinkManager
from cybertools.wiki.dcu.html import Writer as DocutilsHTMLWriter
from cybertools.wiki.dcu.rstx import Parser as DocutilsRstxParser
from cybertools.wiki.dcu import process


class Test(unittest.TestCase):
    "Basic tests for the wiki package."

    def testBasicStuff(self):
        pass


def setUp(testCase):
    component.provideUtility(WikiConfiguration())
    component.provideUtility(DocutilsHTMLWriter(), name='docutils.html')
    component.provideUtility(DocutilsRstxParser(), name='docutils.rstx')
    component.provideAdapter(TreeProcessor, name='standard')
    component.provideAdapter(process.Reference, name='default')
    component.provideUtility(LinkManager(), name='basic')


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        DocFileSuite('README.txt', optionflags=flags, setUp=setUp),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
