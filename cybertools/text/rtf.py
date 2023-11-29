# cybertools.text.rtf

"""Searchable text support for MS Word (.doc) files.

This uses the wvware command to perform the extraction.
Based on code provided by zc.index and TextIndexNG3.
"""

import os, sys
from xml import sax
from io import StringIO

from cybertools.text import base


class RtfTextHandler(sax.ContentHandler):

    def characters(self, text):
        self._data.write(text)

    def startDocument(self):
        self._data = StringIO()

    def startElement(self, name, attrs):
        if name == 'para':
            self._data.write('\n')

    def getData(self):
        return self._data.getvalue()


class RtfTransform(base.BaseFileTransform):

    extension = ".rtf"

    def extract(self, directory, filename):
        if not self.checkAvailable('rtf2xml', 'rtf2xml is not available'):
            return u''
        #xmlstr = self.execute('cd /tmp && rtf2xml --no-dtd "%s"' % filename)
        xmlstr = self.execute('rtf2xml --no-dtd "%s"' % filename)
        handler = RtfTextHandler()
        sax.parseString(xmlstr, handler)
        return handler.getData()
