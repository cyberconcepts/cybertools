#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
from cybertools.text.lib.BeautifulSoup import Declaration, NavigableString

validTags = ('a b br div em font h1 h2 h3 i li ol p pre span strong '
             'table td tr u ul').split()

validAttrs = ('align border cellpadding cellspacing class colspan href rowspan '
              'style title').split()

validStyles = 'font-style font-weight'.split()
validStyleParts = 'border padding'.split()


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
            attr = attr.lower()
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
            if checkStyle(k):
                result.append(item.strip())
    return '; '.join(result)

def checkStyle(k):
    k = k.strip().lower()
    if k in validStyles:
        return True
    for name in validStyleParts:
        if k.startswith(name):
            return True
    return False


def stripAll(value):
    def collectText(tags):
        for tag in tags:
            if type(tag) is NavigableString:
                data.append(tag)
            elif tag is not None and type(tag) is not Declaration:
                collectText(tag.contents)
    data = []
    soup = BeautifulSoup(value)
    collectText(soup.contents)
    text = u''.join(data).replace(u'\n', u'').replace(u'&nbsp;', u' ')
    return text

