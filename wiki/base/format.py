#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Basic Wiki formatting.

$Id$
"""

import re
from zope.interface import implements

from cybertools.wiki.base.link import Link, LinkManager
from cybertools.wiki.interfaces import IFormat, IFormatInstance


class FormatInstance(object):

    #implements(IFormatInstance)

    parent = None

    def __init__(self, context):
        self.context = context

    def unmarshall(self, text):
        return self.parent.linkRegexp.sub(self.processLink, text)

    def processLink(self, match):
        ref, label = match.group(1).split(' ', 1)
        link = Link(self.context, ref)
        link.original = match.group(0)
        link.label = label
        self.parent.manager.registerLink(link)
        return self.parent.linkFormat % (self.parent.internalFormat % link.identifier)

    def marshall(self, text):
        return text

    def display(self, text):
        return text


class BasicFormat(object):

    #implements(IFormat)

    name = 'basic'
    instanceFactory = FormatInstance

    internalRegexp = re.compile(r'!\\\$([_A-Z0-9a-z]+)|{(.+)}')
    internalFormat = '${%s}'
    linkRegexp = re.compile(r'\[\[(.+)\]\]')
    linkFormat = '[[%s]]'

    repository = None

    def __init__(self, manager=None):
        if manager is None:
            manager = LinkManager()
        self.manager = manager

    def getInstance(self, context):
        instance = self.instanceFactory(context)
        instance.parent = self
        return instance
