#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Searchable text support for OpenOffice files.

Based on code provided by zc.index and TextIndexNG3.

$Id$
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
        #fr.close()
        #return [handler.getText()]
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
