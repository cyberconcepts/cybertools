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
        State('new', 'new',
              ('plan', 'accept', 'start', 'work', 'finish', 'modify', 'delegate'),
              color='red'),
        State('planned', 'planned',
              ('plan', 'accept', 'start', 'work', 'finish', 'cancel', 'modify'),
              color='red'),
        State('accepted', 'accepted',
              ('plan', 'accept', 'start', 'work', 'finish', 'cancel', 'modify'),
              color='yellow'),
        State('running', 'running',
              ('work', 'finish', 'cancel', 'modify'),
              color='orange'),
        State('done', 'done',
              ('plan', 'accept', 'start', 'work', 'finish', 'cancel', 'modify'),
              color='lightgreen'),
        State('finished', 'finished',
              ('plan', 'accept', 'start', 'work', 'finish', 'modify', 'close'),
              color='green'),
        State('cancelled', 'cancelled',
              ('plan', 'accept', 'start', 'work', 'modify', 'close'),
              color='grey'),
        State('closed', 'closed', (), color='lightblue'),
        State('replaced', 'replaced', (), color='grey'),
        Transition('plan', 'plan', 'planned'),
        Transition('accept', 'accept', 'accepted'),
        Transition('start', 'start working', 'running'),
        Transition('work', 'work', 'done'),
        Transition('finish', 'finish', 'finished'),
        Transition('cancel', 'cancel', 'cancelled'),
        Transition('modify', 'modify', 'new'),
        Transition('delegate', 'delegate', 'planned'),
        Transition('close', 'close', 'closed'),
        initialState='new')


fieldNames = ['title', 'description', 'start', 'end', 'duration', 'effort',
              'comment', 'party']

# meaning:  - not editable, value=default
#           / not editable, value=None
#           + copy
#           . default (may be empty)

editingRules = dict(
    plan    = {'*':         '++.....+'},
    accept  = {'*':         '++.....-',
               'planned':   '++++++.-',
               'accepted':  '++++++.-'},
    start   = {'*':         '++./...-'},
    work    = {'*':         '++.....-',
               'running':   '+++....-'},
    finish  = {'*':         '++.....-',
               'running':   '+++....-'},
    cancel  = {'*':         '++////./'},
    modify  = {'*':         '++++++++'},
    delegate= {'*':         '++......'},
    close   = {'*':         '++////./'},
)


class WorkItem(Stateful, Track):
    """ A work item that may be stored as a track in a tracking storage.
    """

    implements(IWorkItem)

    statesDefinition = 'organize.workItemStates'

    metadata_attributes = Track.metadata_attributes + ('state',)
    index_attributes = metadata_attributes
    typeName = 'WorkItem'

    initAttributes = set(['party', 'title', 'description', 'start', 'end',
                          'duration', 'effort'])

    def __init__(self, taskId, runId, userName, data):
        super(WorkItem, self).__init__(taskId, runId, userName, data)
        self.state = self.getState()    # make initial state persistent
        self.data['creator'] = userName
        self.data['created'] = self.timeStamp

    def getStatesDefinition(self):
        return component.getUtility(IStatesDefinition, name=self.statesDefinition)

    @property
    def party(self):
        return self.userName

    @property
    def title(self):
        return self.data.get('title') or self.description

    @property
    def duration(self):
        value = self.data.get('duration')
        if value is None:
            start, end = (self.data.get('start'), self.data.get('end'))
            if not None in (start, end):
                value = end - start
        return value

    @property
    def effort(self):
        return self.data.get('effort') or self.duration

    def __getattr__(self, attr):
        if attr not in IWorkItem:
            raise AttributeError(attr)
        return self.data.get(attr)

    def doAction(self, action, userName, **kw):
        currentWorkItems = list(getParent(self).query(runId=self.runId))
        if self != currentWorkItems[-1]:
            raise ValueError("Actions are only allowed on the last item of a run.")
        if action in self.specialActions:
            return self.specialActions[action](self, userName, **kw)
        if action not in [t.name for t in self.getAvailableTransitions()]:
            raise ValueError("Action '%s' not allowed in state '%s'" %
                             (action, self.state))
        if self.state == 'new':
            self.setData(**kw)
            self.doTransition(action)
            self.reindex('state')
            return self
        new = self.createNew(action, userName, **kw)
        if self.state == 'running':
            new.replace(self)
        new.doTransition(action)
        new.reindex('state')
        return new

    def modify(self, userName, **kw):
        if self.state == 'new':
            self.setData(**kw)
            return self
        new = self.createNew('modify', userName, **kw)
        new.replace(self, keepState=True)
        return new

    def delegate(self, userName, **kw):
        new = self.createNew('delegate', userName, **kw)
        new.doTransition('plan')
        new.reindex('state')
        if self.state == 'new':
            self.doTransition('plan')
            self.reindex('state')
        return new

    def close(self, userName, **kw):
        new = self.createNew('close', userName, copyData=False, **kw)
        new.state = 'closed'
        new.reindex('state')
        getParent(self).stopRun(runId=self.runId, finish=True)
        return new

    specialActions = dict(modify=modify, delegate=delegate, close=close)

    def setData(self, **kw):
        if self.state != 'new':
            raise ValueError("Attributes may only be changed in state 'new'.")
        party = kw.pop('party', None)
        if party is not None:
            self.userName = party
            self.reindex('userName')
        start = kw.get('start')
        if start is not None:
            self.timeStamp = start
            self.reindex('timeStamp')
        data = self.data
        for k, v in kw.items():
            data[k] = v

    def createNew(self, action, userName, copyData=True, **kw):
        newData = {}
        if copyData:
            for k in self.initAttributes:
                v = kw.get(k, _not_found)
                if v is _not_found:
                    if action == 'start' and k in ('end',):
                        continue
                    if action in ('work', 'finish') and k in ('duration', 'effort',):
                        continue
                    v = self.data.get(k)
                if v is not None:
                    newData[k] = v
        workItems = IWorkItems(getParent(self))
        new = workItems.add(self.taskId, userName, self.runId, **newData)
        return new

    def replace(self, other, keepState=False):
        if keepState:
            self.state = other.state
            self.reindex('state')
        other.state = 'replaced'
        other.reindex('state')

    def reindex(self, idx=None):
        getParent(self).indexTrack(None, self, idx)


class WorkItems(object):
    """ A tracking storage adapter managing work items.
    """

    implements(IWorkItems)
    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        return self.context[key]

    def __iter__(self):
        return iter(self.context.values())

    def query(self, **criteria):
        if 'task' in criteria:
            criteria['taskId'] = criteria.pop('task')
        if 'party' in criteria:
            criteria['userName'] = criteria.pop('party')
        if 'run' in criteria:
            criteria['runId'] = criteria.pop('run')
        return self.context.query(**criteria)

    def add(self, task, userName, run=0, **kw):
        if not run:
            run = self.context.startRun()
        trackId = self.context.saveUserTrack(task, run, userName, {})
        track = self[trackId]
        track.setData(**kw)
        return track
