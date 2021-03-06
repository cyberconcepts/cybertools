#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
"""

import re

from cybertools.text.lib.BeautifulSoup import BeautifulSoup, Comment
from cybertools.text.lib.BeautifulSoup import Declaration, NavigableString

validTags = ('a b br div em font h1 h2 h3 i img li ol p pre span strong '
             'table td tr u ul').split()

validAttrs = ('align alt border cellpadding cellspacing class colspan '
              'href rowspan src style target title width').split()

validStyles = 'font-style font-weight'.split()
validStyleParts = 'border padding'.split()

escCommPattern = re.compile(r'&lt;\!--\[if .*?\!\[endif\]--&gt;', re.DOTALL)

sentencePattern = re.compile(r'[:.\?\!]')

def sanitize(value, validTags=validTags, validAttrs=validAttrs,
                    validStyles=validStyles, stripEscapedComments=True):
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
    result = soup.renderContents()
    if stripEscapedComments:
        result = escCommPattern.sub(u'', result)
    return result.decode('utf8')


def sanitizeStyle(value, validStyles=validStyles):
    result = []
    for item in value.split(';'):
        if ':' in item:
            #k, v = item.split(':')
            parts = item.split(':')
            if len(parts) == 2:
                k, v = parts
                if checkStyle(k, validStyles):
                    result.append(item.strip())
    return '; '.join(result)

def checkStyle(k, validStyles=validStyles):
    k = k.strip().lower()
    if k in validStyles:
        return True
    for name in validStyleParts:
        if k.startswith(name):
            return True
    return False


def stripComments(value):
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    return soup.renderContents().decode('utf8')


def stripAll(value):
    value = sanitize(value)
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


def extractFirstPart(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name in ('p',):
            part = tag.renderContents()
            break
    else:
        text = stripAll(value)
        part = sentencePattern.split(text)[0]
    if isinstance(part, unicode):
        part = part.encode('UTF-8')
    return ('<p>%s</p>' % part).decode('utf8')
