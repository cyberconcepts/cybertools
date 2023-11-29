# cybertools.text.ooffice

"""Searchable text support for OpenOffice files.

Based on code provided by zc.index and TextIndexNG3.
"""

import os, sys
import xml.sax
import xml.sax.handler
import xml.sax.xmlreader
import zipfile

from cybertools.text import base


class OOTransform(base.BaseFileTransform):

    def __call__(self, fr):
        handler = TextExtractionHandler()
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, True)
        parser.setContentHandler(handler)
        parser.setEntityResolver(entityResolver)
        zf = zipfile.ZipFile(fr, "r")
        parser.feed(zf.read("content.xml"))
        zf.close()
        return handler.getText()


class TextExtractionHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self._buffer = []

    def getText(self):
        return u"".join(self._buffer)

    def ensureWhitespace(self, *args):
        if self._buffer and self._buffer[-1] != u" ":
            self._buffer.append(u" ")

    startElement = ensureWhitespace
    endElement = ensureWhitespace

    startElementNS = ensureWhitespace
    endElementNS = ensureWhitespace

    def characters(self, data):
        self._buffer.append(data)


class EntityResolver(object):

    def resolveEntity(self, publicId, systemId):
        source = xml.sax.xmlreader.InputSource()
        source.setByteStream(cStringIO.StringIO(""))
        source.setEncoding("utf-8")
        source.setPublicId(publicId)
        source.setSystemId(systemId)
        return source

entityResolver = EntityResolver()
