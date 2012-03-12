#
#  Copyright (c) 2012 Helmut Merz helmutm@cy55.de
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
View definitions for generation of documents.
"""

import os
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.publisher.browser import BrowserPage

word_template = ViewPageTemplateFile('word_page.pt')


class Base(BrowserPage):

    encoding = 'UTF-8'
    #encoding = 'ISO8859-15'

    def __call__(self, *args, **kw):
        data = self.index(*args, **kw).encode(self.encoding)
        self.setHeader(data)
        return data


class WordDocument(Base):

    index = word_template
    showLinks = False

    def setHeader(self, data, filename='document'):
        fn = '%s.doc' % filename
        response = self.request.response
        response.setHeader('Cache-Control', '')
        response.setHeader('Pragma', '')
        response.setHeader('Content-Type',
                           'application/msword;charset=%s' % self.encoding)
        response.setHeader('Content-Length', len(data))
        response.setHeader('Content-Disposition', 'filename="%s"' % fn)

    mswordXml = """<xml>
        <w:WordDocument>
        <w:View>Print</w:View>
        <w:Zoom>90</w:Zoom>
        <w:DoNotOptimizeForBrowser />
        </w:WordDocument>
    </xml>"""

    @Lazy
    def css(self):
        fn = os.path.join(os.path.dirname(__file__), 'word.css')
        f = open(fn, 'r')
        css = f.read()
        f.close()
        return css

