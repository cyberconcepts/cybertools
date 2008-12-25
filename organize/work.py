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
from zope.traversing.api import getName, getParent

from cybertools.organize.interfaces import IWorkItem, IWorkItems
from cybertools.stateful.base import Stateful
from cybertools.stateful.definition import StatesDefinition
from cybertools.stateful.definition import State, Transition
from cybertools.stateful.interfaces import IStatesDefinition
from cybertools.tracking.btree import Track, getTimeStamp
from cybertools.tracking.interfaces import ITrackingStorage

_not_found = object()


@implementer(IStatesDefinition)
def workItemStates():
    return StatesDefinition('workItemStates',
        State('created', 'created', ('assign', 'cancel',), color='red'),
        State('assigned', 'assigned', ('start', 'finish', 'cancel', 'transfer'),
              color='yellow'),
        State('running', 'running', ('finish', 'continue', 'cancel', 'transfer'),
              color='orange'),
        State('finished', 'finished', (), color='green'),
        State('continued', 'continued', (), color='blue'),
        State('transferred', 'transferred', (), color='lightblue'),
        State('cancelled', 'cancelled', (), color='grey'),
        Transition('assign', 'assign', 'assigned'),
        Transition('start', 'start', 'running'),
        Transition('finish', 'finish', 'finished'),
        Transition('continue', 'continue', 'continued'),
        Transition('transfer', 'transfer', 'transferred'),
        Transition('cancel', 'cancel', 'cancelled'),
        initialState='created')


class WorkItem(Stateful):

    implements(IWorkItem)

    statesDefinition = 'organize.workItemStates'

    def getStatesDefinition(self):
        return component.getUtility(IStatesDefinition, name=self.statesDefinition)


class WorkItemTrack(WorkItem, Track):
    """ A work item that may be stored as a track in a tracking storage.
    """

    metadata_attributes = Track.metadata_attributes + ('state',)
    index_attributes = metadata_attributes
    typeName = 'WorkItem'

    initAttributes = set(['party', 'description', 'predecessor',
                          'planStart', 'planEnd', 'planDuration', 'planEffort'])

    closeAttributes = set(['end', 'duration', 'effort', 'comment'])

    def __init__(self, taskId, runId, userName, data):
        super(WorkItemTrack, self).__init__(taskId, runId, userName, data)
        self.state = self.getState()    # make initial state persistent
        self.data['creator'] = userName
        self.data['created'] = self.timeStamp

    def __getattr__(self, attr):
        if attr not in IWorkItem:
            raise AttributeError(attr)
        return self.data.get(attr, None)

    @property
    def party(self):
        return self.userName

    def setInitData(self, **kw):
        for k in kw:
            if k not in self.initAttributes:
                raise ValueError("Illegal initial attribute: '%s'." % k)
        party = kw.pop('party', None)
        if party is not None:
            if self.state != 'created':
                raise ValueError("Attribute 'party' may not be set in state '%s'." %
                                 self.state)
            else:
                self.userName = party
                indexChanged = True
        self.checkOverwrite(kw)
        updatePlanData = False
        indexChanged = False
        data = self.data
        for k, v in kw.items():
            data[k] = v
            if k.startswith('plan'):
                updatePlanData = True
        if self.planStart is not None and self.planStart != self.timeStamp:
            self.timeStamp = self.planStart
            indexChanged = True
        if updatePlanData and self.planStart:
            data['planEnd'], data['planDuration'], data['planEffort'] = \
                recalcTimes(self.planStart, self.planEnd,
                            self.planDuration, self.planEffort)
        if indexChanged:
            self.reindex()

    def assign(self, party=None):
        self.doTransition('assign')
        self.data['assigned'] = getTimeStamp()
        if party is not None:
            self.userName = party
        self.reindex()

    def startWork(self, **kw):
        self.checkOverwrite(kw)
        self.doTransition('start')
        start = self.data['start'] = kw.pop('start', None) or getTimeStamp()
        self.timeStamp = start
        self.reindex()

    def stopWork(self, transition='finish', **kw):
        self.doTransition(transition)
        data = self.data
        for k in self.closeAttributes:
            v = kw.pop(k, None)
            if v is not None:
                data[k] = v
        if self.start:
            data['end'], data['duration'], data['effort'] = \
                recalcTimes(self.start, self.end, self.duration, self.effort)
        self.timeStamp = self.end or getTimeStamp()
        self.reindex()
        if transition in ('continue', 'transfer'):
            if transition == 'continue' and kw.get('party') is not None:
                raise ValueError("Setting 'party' is not allowed when continuing.")
            newData = {}
            for k in self.initAttributes:
                v = kw.pop(k, _not_found)
                if v is _not_found:
                    v = data.get(k)
                if v is not None:
                    newData[k] = v
            if transition == 'transfer' and 'party' not in newData:
                raise ValueError("Property 'party' must be set when transferring.")
            workItems = IWorkItems(getParent(self))
            new = workItems.add(self.taskId, self.userName, self.runId, **newData)
            if transition == 'continue':
                new.assign()
            new.data['predecessor'] = self.__name__
            self.data['continuation'] = new.__name__
            return new

    def reindex(self):
        getParent(self).updateTrack(self, {})   # force reindex

    def checkOverwrite(self, kw):
        for k, v in kw.items():
            #old = data.get(k)
            old = getattr(self, k, None)
            if old is not None and old != v:
                raise ValueError("Attribute '%s' already set to '%s'." % (k, old))


def recalcTimes(start, end, duration, effort):
    if duration is None and start and end:
        duration = end - start
    if end is None and start and duration:
        end = start + duration
    if effort is None and duration:
        effort = duration
    return end, duration, effort


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
        trackId = self.context.saveUserTrack(task, run, party, {})
        track = self[trackId]
        track.setInitData(**kw)
        return track
