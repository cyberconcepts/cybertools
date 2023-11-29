# cybertools.text.doc

"""Searchable text support for MS Word (.doc) files.

This uses the wvware command to perform the extraction.
Based on code provided by zc.index and TextIndexNG3.
"""

import os, sys

from cybertools.text import base

try:
    from Globals import package_home
    wvConf = os.path.join(package_home(globals()), 'config', 'wvText.xml')
except ImportError:
    wvConf = os.path.join(os.path.dirname(__file__), 'config', 'wvText.xml')


class DocTransform(base.BaseFileTransform):

    extension = ".doc"

    def extract(self, directory, filename):
        if not self.checkAvailable('wvWare', 'wvWare is not available'):
            return u''
        if sys.platform == 'win32':
            data = self.execute('wvWare -c utf-8 --nographics -x "%s" "%s" 2> nul:'
                                % (wvConf, filename))
        else:
            data = self.execute('wvWare -c utf-8 --nographics -x "%s" "%s" 2> /dev/null'
                                % (wvConf, filename))
        return data
