# cybertools.text.pdf

"""Searchable text support for Portable Document Format (PDF) files.

This uses the pdftotext command from xpdf to perform the extraction.
Based on code provided by zc.index and TextIndexNG3.
"""

import os, sys

from cybertools.text import base


class PdfTransform(base.BaseFileTransform):

    extension = ".pdf"

    def extract(self, directory, filename):
        if not self.checkAvailable('pdftotext', 'pdftotext is not available'):
            return u''
        data = self.execute('pdftotext -enc UTF-8 "%s" -' % filename)
        return data
