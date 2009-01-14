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
Tree processor implementation

$Id$
"""

from zope.interface import implements
from zope.component import adapts
from zope import component

from cybertools.wiki.interfaces import ITreeProcessor, INodeProcessor
from cybertools.wiki.interfaces import IWikiPage


class TreeProcessor(object):
    """ The standard tree processor walking the tree and processing
        the tree's nodes.
    """

    implements(ITreeProcessor)
    adapts(IWikiPage)

    tree = None
    visitor = None

    def __init__(self, context):
        self.context = context

    def process(self):
        self.visitor = visitor = Visitor(self)
        self.tree.walk(visitor)


class Visitor(object):

    def __init__(self, context):
        self.context = context          # the tree processor
        self.document = context.tree    # needed internally
        self.processors = {}            # cache
        self.processorNames = self.context.context.getConfig('nodeProcessors')

    def dispatch_visit(self, node):
        #print 'visiting', node.tagname
        tag = node.tagname
        procs = self.processors.get(tag)
        if procs is None:
            procs = self.processors[tag] = []
            procNames = self.processorNames.get(tag, [])
            for n in procNames:
                proc = component.queryAdapter(node, INodeProcessor, name=n)
                if proc is not None:
                    proc.parent = self.context
                    procs.append(proc)
        for p in procs:
            p.process()
