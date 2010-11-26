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
Basic (sample) implementations for links and link management.

$Id$
"""

from docutils.nodes import Text
from zope.interface import implements
from zope.traversing.browser import absoluteURL

from cybertools.link.interfaces import ILink, ILinkManager
from cybertools.wiki.interfaces import ILinkProcessor


class LinkProcessor(object):
    """ Abstract base class. """

    implements(ILinkProcessor)

    source = request = None
    targetName = ''

    def __init__(self, context):
        self.context = context

    def process(self):
        if '..' in self.targetName:
            return
        wiki = self.source.getWiki()
        manager = wiki.getManager()
        lmName = self.source.getConfig('linkManager')
        lm = manager.getPlugin(ILinkManager, lmName)
        targetPageName = self.targetName
        params = fragment = ''
        if '?' in targetPageName:
            targetPageName, params = targetPageName.split('?', 1)
        if '#' in targetPageName:
            targetPageName, fragment = targetPageName.split('#', 1)
        #existing = iter(lm.query(source=self.source, name=self.targetName))
        for link in lm.query(source=self.source, name=self.targetName):
            #link = existing.next()
            if link.target is not None:
                #target = manager.getObject(link.target)
                target = self.getTarget(manager, wiki, link.target)
            else:
                target = None
            break
        else:
            #target = wiki.getPage(targetPageName)
            target = self.findTarget(manager, wiki, targetPageName)
            link = lm.createLink(name=self.targetName,
                                 source=self.source, target=target)
        if fragment:
            link.targetFragment = fragment
        if params:
            link.targetParameters = params
        if self.request is not None:
            if target is None:
                #uri = link.refuri = '%s/create.html?name=%s' % (
                uri = '%s/@@create.html?name=%s' % (
                                absoluteURL(wiki, self.request), link.name)
            else:
                uri = target.getURI(self.request)
                uri += self.fragmentAndParams(fragment, params)
        self.setURI(uri)
        if target is None:
            self.markPresentation('create')
            self.addText('?')

    def findTarget(self, manager, wiki, name):
        return wiki.getPage(name)

    def getTarget(self, manager, wiki, uid):
        return manager.getObject(uid)

    def fragmentAndParams(self, fragment, params):
        f = p = ''
        if fragment:
            f = '#' + fragment
        if params:
            p = '?' + params
        return f + p

    def setURI(self, uri):
        raise ValueError('To be implemented by subclass.')

    def markPresentation(self, feature):
        raise ValueError('To be implemented by subclass.')

    def addText(self, text):
        raise ValueError('To be implemented by subclass.')

