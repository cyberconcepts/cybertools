"""
Generation and manipulation of XML trees.

$Id$
"""

from cStringIO import StringIO
from lxml import etree


class Generator(object):

    def __getitem__(self, name):
        return Element(name)

    def __getattr__(self, name):
        return self[name]

elements = Generator()


class Element(object):

    def __init__(self, name):
        self.__name__ = name
        self.children = []
        self.attributes = {}

    def __getattr__(self, name):
        if name.endswith('_'):
            name = name[:-1]
        return self[name]

    def __getitem__(self, name):
        el = Element(name)
        self.children.append(el)
        return el

    def __call__(self, *children, **attributes):
        self.children.extend(list(children))
        for a in attributes:
            if a.endswith('_'):
                attr = a[:-1]
                attributes[attr] = attributes[a]
                del attributes[a]
        self.attributes.update(attributes)
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
        elem = etree.Element(self.__name__)
        makeSubTree(elem, self)
        return etree.ElementTree(elem)

    def renderTree(self):
        out = StringIO()
        tree = self.makeTree()
        tree.write(out)
        return out.getvalue()


def makeSubTree(elem, content):
    for a in content.attributes:
        elem.set(a, content.attributes[a])
    subElem = None
    for c in content.children:
        if isinstance(c, Element):
            subElem = etree.SubElement(elem, c.__name__)
            makeSubTree(subElem, c)
        elif subElem is None:
            elem.text = elem.text and '\n'.join(elem.text, c) or c
        else:
            subElem.tail = subElem.tail and '\n'.join(subElem.tail, c) or c


def getElementsFromTree(elem):
    content = Element(elem.tag)
    for key, value in elem.items():
        content.attributes[key] = value
    if elem.text:
        content.children.append(elem.text)
    for child in elem.getchildren():
        content.children.append(getElementsFromTree(child))
        if child.tail:
            content.children.append(child.tail)
    return content


def fromXML(xml):
    elem = etree.XML(xml)
    return getElementsFromTree(elem)
