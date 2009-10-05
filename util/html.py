#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Strip HTML tags and other HTML-related utilities.

$Id$
"""

from cybertools.text.lib.BeautifulSoup import BeautifulSoup, Comment

#validTags = 'p i strong b u a h1 h2 h3 img pre br'.split()
validTags = 'b br div em font h1 h2 h3 i p pre span strong table td tr u'.split()

#validAttrs = 'href src'.split()
validAttrs = 'class style'.split()

validStyles = 'font-style font-weight'.split()


def sanitize(value, validTags=validTags, validAttrs=validAttrs,
                    validStyles=validStyles):
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = []
        for attr, val in tag.attrs:
            if attr not in validAttrs:
                continue
            if attr == 'style':
                val = sanitizeStyle(val, validStyles)
            if val:
                attrs.append((attr, val))
        tag.attrs = attrs
    return soup.renderContents().decode('utf8')


def sanitizeStyle(value, validStyles=validStyles):
    result = []
    for item in value.split(';'):
        if ':' in item:
            k, v = item.split(':')
            if k.strip() in validStyles:
                result.append(item.strip())
    return '; '.join(result)
