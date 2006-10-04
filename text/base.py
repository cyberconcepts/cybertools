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

Based on code provided by zc.index.

$Id$
"""


__docformat__ = "reStructuredText"

import os, shutil, sys, tempfile
from zope.interface import implements
from cybertools.text.interfaces import ITextTransform, IFileTransform

def haveProgram(name):
    """Return true if the program `name` is available."""
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
    return False


class BaseTransform(object):

    implements(ITextTransform)

    def __init__(self, context):
        self.context = context
        self.text = None

    def __call__(self, f):
        if self.text is None:
            fr = open(f, 'r')
            self.text = fr.read()
            fr.close()
        return self.text


class BaseFileTransform(BaseTransform):

    implements(IFileTransform)

    def __call__(self, fr):
        if self.text is None:
            #fr = f.open("rb")
            dirname = tempfile.mkdtemp()
            filename = os.path.join(dirname, "temp" + self.extension)
            try:
                fw = open(filename, "wb")
                shutil.copyfileobj(fr, fw)
                #fr.close()
                fw.close()
                text = self.extract(dirname, filename)
            finally:
                shutil.rmtree(dirname)
            self.text = text
        return self.text

    def extract(self, dirname, filename):
        raise ValueError('Method extract() has to be implemented by subclass.')

