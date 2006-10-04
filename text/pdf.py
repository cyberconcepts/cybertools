"""Searchable text support for Portable Document Format (PDF) files.

This uses the pdftotext command from xpdf to perform the extraction.

"""
__docformat__ = "reStructuredText"

import os, sys

from cybertools.text import base


class PdfTransform(base.BaseFileTransform):

    extension = ".pdf"

    def extract(self, directory, filename):
        if not base.haveProgram("pdftotext"):
            print 'Warning: pdftotext is not available'
            return u''
        txtfile = os.path.join(directory, "words.txt")
        st = os.system("pdftotext -enc UTF-8 %s %s" % (filename, txtfile))
        f = open(txtfile, "rb")
        data = f.read()
        f.close()
        return unicode(data, "utf-8")
