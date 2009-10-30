#! /usr/bin/python

"""
Tests for the 'cybertools.wiki' package.

$Id$
"""

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite
from zope import component
from zope.interface import implements
from zope.app.intid.interfaces import IIntIds
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.browser.interfaces import IAbsoluteURL

from cybertools.relation.tests import IntIdsStub
from cybertools.wiki.base.config import WikiConfiguration
from cybertools.wiki.base.link import LinkManager
from cybertools.wiki.dcu.html import Writer as DocutilsHTMLWriter
from cybertools.wiki.dcu.rstx import Parser as DocutilsRstxParser
from cybertools.wiki.dcu import process
from cybertools.wiki.interfaces import IWiki, IWikiPage
from cybertools.wiki.tracking import link


class WikiURL(object):

    implements(IAbsoluteURL)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return '%s/%s' % (self.request.URL, self.context.name)


class PageURL(WikiURL):

    def __call__(self):
        return '%s/%s' % (WikiURL(self.context.getWiki(), self.request)(),
                          self.context.name)


class Test(unittest.TestCase):
    "Basic tests for the wiki package."

    def testBasicStuff(self):
        pass


def setUp(testCase):
    component.provideAdapter(WikiURL, (IWiki, IBrowserRequest), IAbsoluteURL)
    component.provideAdapter(PageURL, (IWikiPage, IBrowserRequest), IAbsoluteURL)
    component.provideUtility(IntIdsStub())
    component.provideUtility(WikiConfiguration())
    component.provideUtility(DocutilsHTMLWriter(), name='docutils.html')
    component.provideUtility(DocutilsRstxParser(), name='docutils.rstx')
    component.provideAdapter(process.Reference, name='default')
    component.provideUtility(LinkManager(), name='basic')
    component.provideAdapter(link.LinkManager)
    links = link.setupLinkManager(None)
    component.provideUtility(links, name='tracking')
    from cybertools.wiki.generic import wiki
    wiki.IntIds = IntIdsStub


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        DocFileSuite('README.txt', optionflags=flags, setUp=setUp),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
