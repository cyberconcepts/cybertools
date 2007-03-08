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
Searchable text support for MS Word (.doc) files.

This uses the wvware command to perform the extraction.

Based on code provided by zc.index and TextIndexNG3.

$Id$
"""

import os, sys
from xml import sax
from cStringIO import StringIO

from cybertools.text import base


class RtfTextHandler(sax.ContentHandler):

    def characters(self, text):
        self._data.write(text.encode('UTF-8'))

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
        return handler.getData().decode('UTF-8')
