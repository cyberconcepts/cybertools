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
from cybertools.text.lib.BeautifulSoup import BeautifulSoup
from cybertools.text.lib.BeautifulSoup import Declaration, NavigableString


class HtmlTransform(base.BaseTransform):

    def __call__(self, fr):
        input = fr.read().decode('UTF-8')
        return htmlToText(input)


def htmlToText(input):
    data = []
    input = input.replace(u'<!--', u'')
    soup = BeautifulSoup(input)
    collectText(soup.contents, data)
    text = u' '.join(data).replace(u'\n', u'').replace(u'&nbsp;', u'')
    return text

def collectText(tags, data):
    for tag in tags:
        if type(tag) is NavigableString:
            data.append(tag)
        elif tag is not None and type(tag) is not Declaration:
            collectText(tag.contents, data)
