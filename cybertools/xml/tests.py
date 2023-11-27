#! /usr/bin/python

"""
Tests for the 'cyberdev.xml' package.
"""

import unittest, doctest
from cStringIO import StringIO

from cybertools.xml.element import elements as e, fromXML


class TestXml(unittest.TestCase):
    "Basic tests for the xml package."

    baseHtml = e.html(
            e.head(e.title(u'Page Title')),
            e.body(
              e.div(u'The top bar', class_='top'),
              e.div(u'The body stuff', class_='body'),
        ))

    def testBasicStuff(self):
        doc = self.baseHtml
        tree = doc.makeTree()
        out = StringIO()
        tree.write(out)
        text = out.getvalue()

    def testParsing(self):
        xml = ('<html><head><title>Page Title</title></head>'
               '<body><div class="top">The top bar</div>'
               '<div class="body">The body stuff</div></body></html>')
        doc = fromXML(xml)
        text = doc.render()


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                doctest.DocFileSuite('README.txt', optionflags=flags),
                unittest.makeSuite(TestXml),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
