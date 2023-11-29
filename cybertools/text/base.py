# cybertools.text.base

"""Base classes for text transformations.

Based on code provided by zc.index and TextIndexNG3.
"""


import os, shutil, sys, tempfile
import logging
from zope.interface import implementer
from cybertools.text.interfaces import ITextTransform, IFileTransform


@implementer(ITextTransform)
class BaseTransform(object):

    def __init__(self, context):
        self.context = context
        self.text = None

    def __call__(self, fr):
        if self.text is None:
            self.text = fr.read()
        return self.text


@implementer(IFileTransform)
class BaseFileTransform(BaseTransform):

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
            logging.getLogger('zope.server').warning(logMessage)
        return False
