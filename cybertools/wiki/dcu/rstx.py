# cybertools.wiki.dcu.rstx

""" A parser implementation based on the docutils restructured text parser.
"""

from docutils.core import publish_doctree
from zope.interface import implementer

from cybertools.wiki.interfaces import IParser


@implementer(IParser)
class Parser(object):

    def parse(self, text, context=None, request=None):
        tree = publish_doctree(text)
        tree.context = context
        tree.request = request
        return tree
