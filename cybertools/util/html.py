# cybertools.util.html

""" Strip HTML tags and other HTML-related utilities.
"""

import re

#from cybertools.text.lib.BeautifulSoup import BeautifulSoup, Comment
#from cybertools.text.lib.BeautifulSoup import Declaration, NavigableString
from bs4 import BeautifulSoup, Comment, Declaration, NavigableString

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
    soup = BeautifulSoup(value, features='lxml')
    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = {}
        for attr, val in tag.attrs.items():
            attr = attr.lower()
            if attr not in validAttrs:
                continue
            if attr == 'style':
                val = sanitizeStyle(val, validStyles)
            if val:
                attrs[attr] = val
        tag.attrs = attrs
    result = soup.renderContents().decode('UTF-8')
    if stripEscapedComments:
        result = escCommPattern.sub('', result)
    return result


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
    soup = BeautifulSoup(value, features='lxml')
    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
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
    soup = BeautifulSoup(value, features='lxml')
    collectText(soup.contents)
    text = ''.join(data).replace('\n', '').replace('&nbsp;', ' ')
    return text


def extractFirstPart(value):
    soup = BeautifulSoup(value, features='lxml')
    for tag in soup.findAll(True):
        if tag.name in ('p',):
            part = tag.renderContents()
            break
    else:
        text = stripAll(value)
        part = sentencePattern.split(text)[0]
    #if isinstance(part, str):
    #   part = part.encode('UTF-8')
    if isinstance(part, bytes):
        part = part.decode('UTF-8')
    return ('<p>%s</p>' % part) #.decode('utf8')
