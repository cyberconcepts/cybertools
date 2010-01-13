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
Planning and recording activities (work items).

$Id$
"""

from zope import component
from zope.component import adapts
from zope.interface import implementer, implements
from zope.traversing.api import getName, getParent

from cybertools.stateful.base import Stateful
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStatesDefinition
from cybertools.tracking.btree import TrackingStorage, Track
from cybertools.tracking.interfaces import ITrackingStorage
from cybertools.link.base import Link as BaseLink
from cybertools.link.base import LinkManager as BaseLinkManager
from cybertools.wiki.interfaces import ILink, ILinkManager


@implementer(IStatesDefinition)
def linkStates():
    return StatesDefinition('wiki.linkStates',
        State('valid', 'valid', ('invalidate',), color='green'),
        State('invalid', 'invalid', ('validate',), color='red'),
        # transitions:
        Transition('invalidate', 'invalidate', 'invalid'),
        Transition('validate', 'validate', 'valid'),
        initialState='valid')


class Link(BaseLink, Stateful, Track):
    """ A link that is stored as a track in a tracking storage.
    """

    statesDefinition = 'wiki.linkStates'

    metadata_attributes = Track.metadata_attributes + ('name', 'targetId')
    index_attributes = metadata_attributes
    typeName = 'Link'

    def __init__(self, taskId, runId, userName, data={}):
        self.name = data.pop('name', '???')
        self.targetId = data.pop('targetId', '')
        Track.__init__(self, taskId, runId, userName, data={})

    @property
    def identifier(self):
        return self.__name__
        #return getName(self)

    @property
    def source(self):
        return self.taskId

    @property
    def target(self):
        return self.targetId

    def __getattr__(self, k):
        if k not in ILink:
            raise AttributeError(k)
        return self.data.get(k)

    def getManager(self):
        return getParent(self)

    # IStateful

    def getStatesDefinition(self):
        return component.getUtility(IStatesDefinition, name=self.statesDefinition)


class xx_LinkManager(BaseLinkManager):
    """ A tracking storage adapter managing wiki links.
    """

    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def getLink(self, identifier):
        return self.context.get(identifier)

    def query(self, source=None, target=None, name=None, **kw):
        criteria = kw
        if source is not None:
            criteria['taskId'] = source
        if target is not None:
            criteria['targetId'] = target
        if name is not None:
            criteria['name'] = name
        return self.context.query(**criteria)

    def createLink(self, name, source, target, **kw):
        taskId = source
        runId = kw.pop('runId', 0) or 0
        userName = kw.pop('userName', '') or ''
        if not runId:
            runId = self.context.startRun()
        kw['name'] = name
        kw['targetId'] = target
        trackId = self.context.saveUserTrack(taskId, runId, userName, kw)
        track = self.context[trackId]
        return track

    def removeLink(self, link):
        id = link.identifier
        if id in self.context:
            del self.context[id]

    @property
    def links(self):
        return self.context


# for testing only:
def setupLinkManager(manager):
    ts = TrackingStorage(trackFactory=Link)
    return ILinkManager(ts)
