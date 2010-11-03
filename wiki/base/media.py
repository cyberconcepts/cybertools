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
Basic (sample) implementation for a wiki media manager and media objects.

$Id$
"""

from zope.component import adapts
from zope.interface import implements
from cybertools.wiki.interfaces import IWiki, IMediaManager, IMediaObject


class WikiMediaManager(object):
    """ A Wiki adapter for providing media manager functionality. """

    implements(IMediaManager)
    adapts(IWiki)

    name = '.media'
    title = 'Wiki Media Manager'

    def __init__(self, context):
        self.context = context
        objects = getattr(context, '_media', None)
        if objects is None:
            objects = context._media = {}
        self.objects = objects

    def getWiki(self):
        return self.context

    def createObject(self, name, title=None):
        obj = MediaObject(name, title=title, parent=self.context)
        self.objects[name] = obj
        return obj

    def removeObject(self, name):
        del self.objects[name]

    def getObject(self, name):
        return self.objects.get(name)

    def listObjects(self):
        return self.objects.values()


class MediaObject(object):
    """ A basic (maybe persistent) media object. """

    implements(IMediaObject)

    data = None

    def __init__(self, name, title=None, parent=None):
        self.name = name
        self.title = title or Name
        self.parent = parent

    def getManager(self):
        if self.parent is None:
            return None
        mmName = self.parent.getConfig('mediaManager')
        return component.getAdapter(self.parent, IMediaManager, name=mmName)

    def getRawData(self):
        return self.data

    def setRawData(self, data):
        self.data = data
