# cybertools.text.ppt

"""Searchable text support for PowerPoint (.ppt) files.

This uses the ppthtml command from PowerPoint to perform the extraction.
Note: ppthtml is no longer available on current Debian or Ubuntu versions.
Based on code provided by zc.index and TextIndexNG3.
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
