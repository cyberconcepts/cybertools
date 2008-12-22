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
Planning and recording activities (work items).

$Id$
"""

from zope import component
from zope.component import adapts
from zope.interface import implementer, implements

from cybertools.organize.interfaces import IWorkItem, IWorkItems
from cybertools.stateful.base import Stateful
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStatesDefinition
from cybertools.tracking.btree import Track
from cybertools.tracking.interfaces import ITrackingStorage


@implementer(IStatesDefinition)
def workItemStates():
    return StatesDefinition('workItemStates',
        State('created', 'created', ('assign', 'cancel',), color='red'),
        State('assigned', 'assigned', ('start', 'finish', 'cancel', 'transfer'),
              color='yellow'),
        State('running', 'running', ('finish',), color='green'),
        State('finished', 'finished', (), color='blue'),
        State('transferred', 'transferred', (), color='grey'),
        State('cancelled', 'cancelled', (), color='grey'),
        Transition('assign', 'assign', 'assigned'),
        Transition('start', 'start', 'running'),
        Transition('finish', 'finish', 'finished'),
        Transition('transfer', 'transfer', 'transferred'),
        Transition('cancel', 'cancel', 'cancelled'),
        initialState='created')


class WorkItem(Stateful):

    implements(IWorkItem)

    statesDefinition = 'organize.workItemStates'

    def getStatesDefinition(self):
        return component.getUtility(IStatesDefinition, name=self.statesDefinition)

    # work item attributes (except state that is provided by stateful


class WorkItemTrack(WorkItem, Track):
    """ A work item that may be stored as a track in a tracking storage.
    """

    metadata_attributes = Track.metadata_attributes + ('state',)
    index_attributes = metadata_attributes
    typeName = 'WorkItem'

    initAttributes = set(['description', 'predecessor',
                          'planStart', 'planEnd', 'planDuration', 'planEffort'])

    def __init__(self, taskId, runId, userName, data={}):
        for k in data:
            if k not in initAttributes:
                raise ValueError("Illegal initial attribute: '%s'." % k)
        super(WorkItemTrack, self).__init__(taskId, runId, userName, data)
        self.state = self.getState()    # make initial state persistent

    def __getattr__(self, attr):
        value = self.data.get(attr, _not_found)
        if value is _not_found:
            raise AttributeError(attr)
        return value


class WorkItems(object):
    """ A tracking storage adapter managing work items.
    """

    implements(IWorkItems)
    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        return self.context[key]

    def add(self, task, party, run=0, **kw):
        trackId = self.context.saveUserTrack(task, run, party, kw)
        return self[trackId]
