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
Node processor implementations for docutils nodes.

$Id$
"""

from docutils.nodes import reference
from zope.interface import implements
from zope.component import adapts

from cybertools.wiki.interfaces import INodeProcessor, ILinkManager


class Reference(object):

    implements(INodeProcessor)
    adapts(reference)

    parent = None                   # parent (tree) processor

    def __init__(self, context):
        self.node = self.context = context

    def process(self):
        print 'processing reference:', self.node
        source = self.parent.context
        wiki = source.getWiki()
        sourceName = ':'.join((wiki.name, source.name))
        targetName = self.node['refuri']
        lmName = source.getConfig('linkManager')
        lm = wiki.getManager().getPlugin(ILinkManager, lmName)
        target = wiki.getPage(targetName)

