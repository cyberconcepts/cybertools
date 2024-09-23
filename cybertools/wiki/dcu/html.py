# cybertools.wiki.dcu.html

""" A writer implementation based on the docutils HTML writer.
"""

from docutils.core import publish_from_doctree
from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator, Writer as HTMLWriter
from zope import component
from zope.interface import implementer

from cybertools.wiki.interfaces import INodeProcessor, IWriter


class HTMLWriter(HTMLWriter):

    def apply_template(self):
        template = '%(body_pre_docinfo)s\n%(docinfo)s\n%(body)s'
        subs = self.interpolation_dict()
        return template % subs


@implementer(IWriter)
class Writer(object):

    def __init__(self):
        self.writer = HTMLWriter()
        self.writer.translator_class = BodyTranslator

    def write(self, tree):
        return publish_from_doctree(tree, writer=self.writer,
                                    settings_overrides={'embed_stylesheet': False})


class BodyTranslator(HTMLTranslator):

    def astext(self):
        return u''.join(self.body_pre_docinfo + self.docinfo + self.body)

    def visit_image(self, node):
        # copied from docutils.writers.html4css1
        atts = {}
        atts['src'] = node['uri']
        # TODO: provide processing of other attributes
        suffix = '\n'
        self.context.append('')
        htmlNode = HTMLImageNode(self.document, node, atts)
        self.processNode(htmlNode)
        self.body.append(self.emptytag(node, 'img', suffix, **atts))

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


class HTMLImageNode(HTMLNode):

    pass
