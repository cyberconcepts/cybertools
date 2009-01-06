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
A writer implementation based on the docutils HTML writer.

$Id$
"""

from docutils.core import publish_from_doctree
from docutils.writers.html4css1 import HTMLTranslator, Writer as HTMLWriter
from zope.interface import implements

from cybertools.wiki.interfaces import IWriter


class Writer(object):

    implements(IWriter)

    def __init__(self):
        self.writer = HTMLWriter()
        self.writer.translator_class = HTMLBodyTranslator

    def write(self, tree):
        return publish_from_doctree(tree, writer=self.writer)


class HTMLBodyTranslator(HTMLTranslator):

    def astext(self):
        return u''.join(self.body_pre_docinfo + self.docinfo + self.body)
