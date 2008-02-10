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
Searchable text support for Portable Document Format (PDF) files.

This uses the pdftotext command from xpdf to perform the extraction.
interface definitions for text transformations.

Based on code provided by zc.index and TextIndexNG3.

$Id$
"""

import os, sys

from cybertools.text import base
from cybertools.text.html import htmlToText


class PptTransform(base.BaseFileTransform):

    extension = ".ppt"

    def extract(self, directory, filename):
        if not self.checkAvailable('ppthtml', 'ppthtml is not available'):
            return u''
        if sys.platform == 'win32':
            html = self.execute('ppthtml "%s" 2> nul:' % filename)
        else:
            html = self.execute('ppthtml "%s" 2> /dev/null' % filename)
        data = htmlToText(html)
        return data
        #return data.decode('ISO8859-15')
