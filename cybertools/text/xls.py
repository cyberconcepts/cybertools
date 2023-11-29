# cybertools.text.xls

"""Searchable text support for MS Excel (.xls) files.

This uses the xls2csv command to perform the extraction.
Based on code provided by zc.index and TextIndexNG3.
"""

import os, sys

from cybertools.text import base


class XlsTransform(base.BaseFileTransform):

    extension = ".xls"

    def extract(self, directory, filename):
        if not self.checkAvailable('xls2csv', 'xls2csv is not available'):
            return u''
        if sys.platform == 'win32':
            data = self.execute('xls2csv -d 8859-1 -q 0 "%s" 2> nul:' % filename)
        else:
            data = self.execute('xls2csv -d 8859-1 -q 0 "%s" 2> /dev/null' % filename)
        return data
