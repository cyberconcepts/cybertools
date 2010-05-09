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
A writer implementation based on the docutils HTML writer.

$Id$
"""

from docutils.core import publish_from_doctree
from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator, Writer as HTMLWriter
from zope import component
from zope.interface import implements

from cybertools.wiki.interfaces import INodeProcessor, IWriter


class Writer(object):

    implements(IWriter)

    def __init__(self):
        self.writer = HTMLWriter()
        self.writer.translator_class = BodyTranslator

    def write(self, tree):
        return publish_from_doctree(tree, writer=self.writer,
                                    settings_overrides={'embed_stylesheet': False})


class BodyTranslator(HTMLTranslator):

    def astext(self):
        return u''.join(self.body_pre_docinfo + self.docinfo + self.body)

    def visit_reference(self, node):
        # copied from docutils.writers.html4css1
        if node.has_key('refuri'):
            href = node['refuri']
            if (self.settings.cloak_email_addresses
                 and href.startswith('mailto:')):
                href = self.cloak_mailto(href)
                self.in_mailto = 1
        else:
            assert node.has_key('refid'), \
                   'References must have "refuri" or "refid" attribute.'
            href = '#' + node['refid']
        atts = {'href': href, 'class': 'reference'}
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        # wiki processing
        htmlNode = HTMLReferenceNode(self.document, node, atts)
        self.processNode(htmlNode)
        self.body.append(self.starttag(node, 'a', '', **atts))

    def processNode(self, htmlNode):
        processorNames = self.document.context.getConfig('nodeProcessors')
        procNames = processorNames.get(htmlNode.node.tagname, [])
        for n in procNames:
            proc = component.queryAdapter(htmlNode, INodeProcessor, name=n)
            if proc is not None:
                proc.process()


class HTMLNode(object):

    def __init__(self, document, node, atts):
        self.document = document
        self.node = node
        self.atts = atts


class HTMLReferenceNode(HTMLNode):

    pass
