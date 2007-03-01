#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
Base classes for text transformations.

Based on code provided by zc.index and TextIndexNG3.

$Id$
"""


import os, shutil, sys, tempfile
import logging
from zope.interface import implements
from cybertools.text.interfaces import ITextTransform, IFileTransform


class BaseTransform(object):

    implements(ITextTransform)

    def __init__(self, context):
        self.context = context
        self.text = None

    def __call__(self, fr):
        if self.text is None:
            self.text = fr.read()
        return self.text


class BaseFileTransform(BaseTransform):

    implements(IFileTransform)

    extension = '.txt'

    def __call__(self, fr):
        if self.text is None:
            dirname = tempfile.mkdtemp()
            filename = os.path.join(dirname, "temp" + self.extension)
            try:
                fw = open(filename, "wb")
                shutil.copyfileobj(fr, fw)
                fw.close()
                text = self.extract(dirname, filename)
            finally:
                shutil.rmtree(dirname)
                #fr.close()
            self.text = text
        return self.text

    def extract(self, dirname, filename):
        raise ValueError('Method extract() has to be implemented by subclass.')

    def execute(self, com):
        try:
            import win32pipe
            result = win32pipe.popen(com).read()
        except ImportError:
            result = os.popen(com).read()
        return result

    def checkAvailable(self, name, logMessage=''):
        if sys.platform.lower().startswith("win"):
            extensions = (".com", ".exe", ".bat")
        else:
            extensions = ("",)
        execpath = os.environ.get("PATH", "").split(os.path.pathsep)
        for path in execpath:
            for ext in extensions:
                fn = os.path.join(path, name + ext)
                if os.path.isfile(fn):
                    return True
        if logMessage:
            logging.getLogger('zope.server').warn(logMessage)
        return False
