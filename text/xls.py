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
Searchable text support for MS Excel (.xls) files.

This uses the xls2csv command to perform the extraction.

Based on code provided by zc.index and TextIndexNG3.

$Id$
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
        return data.decode('ISO8859-1')
