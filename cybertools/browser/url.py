# cybertools.browser.url

""" URL manipulation utilities
"""

from urlparse import urlparse

from zope.container.traversal import ItemTraverser
from zope.interface import Interface, implements


class TraversalRedirector(ItemTraverser):

    port = 9083
    names = ('ctt', 'sona',)
    loc_pattern = 'www.%s.de'
    skip = (0, 4)

    def publishTraverse(self, request, name):
        return super(TraversalRedirector, self).publishTraverse(request, name)
