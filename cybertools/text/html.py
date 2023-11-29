# cybertools.text.html

"""Searchable text support for HTML files.
"""

import os, sys

from cybertools.text import base
from bs4 import BeautifulSoup, Declaration, Doctype, NavigableString


class HtmlTransform(base.BaseTransform):

    def __call__(self, fr):
        input = fr.read().decode('UTF-8')
        return htmlToText(input)


def htmlToText(input):
    data = []
    input = input.replace(u'<!--', u'')
    soup = BeautifulSoup(input, features='lxml')
    collectText(soup.contents, data)
    text = u' '.join(data).replace(u'\n', u'').replace(u'&nbsp;', u'')
    return text

def collectText(tags, data):
    for tag in tags:
        if type(tag) is NavigableString:
            data.append(tag)
        elif tag is not None and type(tag) not in (Declaration, Doctype):
            collectText(tag.contents, data)
