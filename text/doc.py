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
        return data.decode('UTF-8')
