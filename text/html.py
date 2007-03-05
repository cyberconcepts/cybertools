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
Searchable text support for HTML files.

$Id$
"""

import os, sys
from cStringIO import StringIO

from cybertools.text import base
from cybertools.text.lib.BeautifulSoup import BeautifulSoup, NavigableString


def htmlToText(html):
    data = []
    soup = BeautifulSoup(html).html
    collectText([soup], data)
    text = u' '.join(data).replace('\n', '').replace('&nbsp;', '')
    return text

def collectText(tags, data):
    for tag in tags:
        if type(tag) is NavigableString:
            data.append(tag)
        else:
            collectText(tag.contents, data)
