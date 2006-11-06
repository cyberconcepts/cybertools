"""
Generation and manipulation of XML trees.

$Id$
"""

from cStringIO import StringIO
from lxml import etree


class Generator(object):

    def __getitem__(self, name):
        return Element(etree.Element(name))

    def __getattr__(self, name):
        return self[name]

elements = Generator()


class Element(object):

    def __init__(self, baseElement):
        self.baseElement = baseElement

    @property
    def __name__(self):
        return self.baseElement.tag

    @property
    def children(self):
        base = self.baseElement
        result = []
        if base.text:
            result.append(base.text)
        for c in base.getchildren():
            result.append(Element(c))
        if base.tail:
            result.append(base.tail)
        return result

    @property
    def attributes(self):
        return self.baseElement.attrib

    def __getattr__(self, name):
        if name.endswith('_'):
            name = name[:-1]
        return self[name]

    def __getitem__(self, name):
        elem = etree.Element(name)
        self.baseElement.append(elem)
        return Element(elem)

    def __call__(self, *children, **attributes):
        base = self.baseElement
        for c in children:
            if isinstance(c, Element):
                base.append(c.baseElement)
            elif not base:
                base.text = base.text and '\n'.join(base.text, c) or c
            else:
                base.tail = base.tail and '\n'.join(base.tail, c) or c
        for a in attributes:
            if a.endswith('_'):
                attr = a[:-1]
                attributes[attr] = attributes[a]
                del attributes[a]
        for a in attributes:
            base.attrib[a] = attributes[a]
        return self

    def render(self, level=0):
        out = StringIO()
        out.write('  ' * level)
        out.write('<' + self.__name__)
        for a in self.attributes:
            attr = a
            if attr.endswith('_'):
                attr = attr[:-1]
            out.write(' %s="%s"' % (attr, self.attributes[a]))
        out.write('>\n')
        for e in self.children:
            if isinstance(e, Element):
                out.write(e.render(level+1))
            else:
                out.write('  ' * (level+1))
                out.write(e)
                out.write('\n')
        out.write('  ' * level)
        out.write('</%s>' % self.__name__)
        out.write('\n')
        return out.getvalue()

    def makeTree(self):
        return etree.ElementTree(self.baseElement)

    def renderTree(self):
        out = StringIO()
        tree = self.makeTree()
        tree.write(out)
        return out.getvalue()


def fromXML(xml):
    elem = etree.XML(xml)
    return Element(elem)
