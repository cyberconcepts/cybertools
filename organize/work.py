#
#  Copyright (c) 2016 Helmut Merz helmutm@cy55.de
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
from cybertools.util.jeep import Jeep

_not_found = object()


@implementer(IStatesDefinition)
def workItemStates():
    return StatesDefinition('workItemStates',
        State('new', 'new',
              ('plan', 'accept', 'start', 'work', 'finish', 'delegate',
               'cancel', 'reopen'),     # 'move', # ?
              color='red'),
        State('planned', 'planned',
              ('plan', 'accept', 'start', 'work', 'finish', 'delegate',
               'move', 'cancel', 'modify'), color='red'),
        State('accepted', 'accepted',
              ('plan', 'accept', 'start', 'work', 'finish',
               'move', 'cancel', 'modify'),
              color='yellow'),
        State('running', 'running',
              ('work', 'finish', 'move', 'cancel', 'modify'),   # 'delegate', # ?
              color='orange'),
        State('done', 'done',
              ('plan', 'accept', 'start', 'work', 'finish', 'delegate',
               'move', 'cancel', 'modify'), color='lightgreen'),
        State('finished', 'finished',
              ('plan', 'accept', 'start', 'work', 'finish',
               'move', 'modify', 'close', 'cancel'),
              color='green'),
        State('cancelled', 'cancelled',
              ('plan', 'accept', 'start', 'work', 'move', 'modify', 'close'),
              color='grey'),
        State('closed', 'closed', ('reopen',), color='lightblue'),
        # not directly reachable states:
        State('delegated', 'delegated',
              ('plan', 'accept', #'start', 'work', 'finish', 
               'close', 'delegate', 'move', 'cancel', 'modify'),
              color='purple'),
        State('delegated_x', 'delegated', (), color='purple'),
        State('moved', 'moved',
              ('plan', 'accept', 'start', 'work', 'finish', 'close', 
               'delegate', 'move', 'cancel', 'modify'),
              color='grey'),
        State('moved_x', 'moved', (), color='grey'),
        State('replaced', 'replaced', (), color='grey'),
        State('planned_x', 'planned', (), color='red'),
        State('accepted_x', 'accepted', (), color='yellow'),
        State('done_x', 'done', 
              ('modify', 'move', 'cancel'), color='lightgreen'),
        State('finished_x', 'finished', 
              ('modify','move', 'cancel'), color='green'),
        #State('done_y', 'done', (), color='grey'),
        #State('finished_y', 'finished', (), color='grey'),
        # transitions:
        Transition('plan', 'plan', 'planned'),
        Transition('accept', 'accept', 'accepted'),
        Transition('start', 'start working', 'running'),    # obsolete?
        Transition('work', 'work', 'done'),
        Transition('finish', 'finish', 'finished'),
        Transition('cancel', 'cancel', 'cancelled'),
        Transition('modify', 'modify', 'new'),
        Transition('delegate', 'delegate', 'planned'),
        Transition('move', 'move', 'planned'),
        Transition('close', 'close', 'closed'),
        Transition('reopen', 're-open', 'planned'),
        initialState='new')


fieldNames = ['title', 'description', 'deadline', 'priority', 'activity',
              'start', 'end', 
              'duration', 'effort',
              'comment', 'party']   # for use in editingRules

# meaning:  - not editable, value=default
#           / not editable, value=None
#           + copy
#           . default (may be empty)

editingRules = dict(
    plan    = {'*':         '+++++.....+'},
    accept  = {'*':         '+++++.....-',
               'planned':   '+++++++++.-',
               'accepted':  '+++++++++.-'},
    start   = {'*':         '+++++./...-'},
    work    = {'*':         '+++++.....-',
               'running':   '++++++....-'},
    finish  = {'*':         '+++++.....-',
               'running':   '++++++....-'},
    cancel  = {'*':         '+++++////./'},
    modify  = {'*':         '+++++++++++'},
    delegate= {'*':         '+++++++++.+'},
    move    = {'*':         '+++++++++.-'},
    close   = {'*':         '+++++////./'},
    reopen  = {'*':         '+++++////./'},
)


class WorkItemType(object):
    """ Specify the type of a work item.

        The work item type controls which actions (transitions)
        and fields are available for a certain work item.
    """

    def __init__(self, name, title, description=u'', 
                 actions=None, fields=None, indicator=None,
                 delegatedState='delegated', prefillDate=True):
        self.name = name
        self.title = title
        self.description = description
        self.actions = actions or list(editingRules)
        self.fields = fields or ('deadline', 'priority', 'activity', 
                                 'start-end', 'duration-effort')
        self.indicator = indicator
        self.delegatedState = delegatedState
        self.prefillDate = prefillDate

workItemTypes = Jeep((
    WorkItemType('work', u'Unit of Work', indicator='work_work'),
    WorkItemType('scheduled', u'Scheduled Event',
        actions=('plan', 'accept', 'finish', 'cancel', 
                 'modify', 'delegate', 'move', 'close', 'reopen'),
        fields =('start-end', 'duration-effort',),
        indicator='work_event'),
    WorkItemType('deadline', u'Deadline',
        actions=('plan', 'accept', 'finish', 'cancel', 
                 'modify', 'delegate', 'move', 'close', 'reopen'),
        fields =('deadline',),
        indicator='work_deadline'),
    WorkItemType('checkup', u'Check-up',
        actions=('plan', 'accept', 'start', 'finish', 'cancel', 
                 'modify', 'delegate', 'close', 'reopen'),
        #fields =('deadline', 'start-end',),
        fields =('deadline', 'daterange',),
        indicator='work_checkup',
        delegatedState='closed', prefillDate=False),
))


class WorkItem(Stateful, Track):
    """ A work item that may be stored as a track in a tracking storage.
    """

    implements(IWorkItem)

    metadata_attributes = Track.metadata_attributes + ('state',)
    index_attributes = metadata_attributes
    typeName = 'WorkItem'
    typeInterface = IWorkItem
    statesDefinition = 'organize.workItemStates'

    initAttributes = set(['workItemType', 'party', 'title', 'description', 
                          'deadline', 'priority', 'activity', 'start', 'end',
                          'duration', 'effort'])

    def __init__(self, taskId, runId, userName, data):
        super(WorkItem, self).__init__(taskId, runId, userName, data)
        self.state = self.getState()    # make initial state persistent
        self.data['creator'] = userName
        self.data['created'] = self.timeStamp

    def getStatesDefinition(self):
        return component.getUtility(IStatesDefinition, 
                                    name=self.statesDefinition)

    def getWorkItemType(self):
        name = self.workItemType
        return name and workItemTypes[name] or workItemTypes['work']

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
        if attr not in self.typeInterface:
            raise AttributeError(attr)
        return self.data.get(attr)

    @property
    def currentWorkItems(self):
        return list(getParent(self).query(runId=self.runId))

    def doAction(self, action, userName, **kw):
        #if self != self.currentWorkItems[-1]:
        #    raise ValueError("Actions are only allowed on the last item of a run.")
        if action not in [t.name for t in self.getAvailableTransitions()]:
            raise ValueError("Action '%s' not allowed in state '%s'" %
                             (action, self.state))
        if action in self.specialActions:
            return self.specialActions[action](self, userName, **kw)
        return self.doStandardAction(action, userName, **kw)

    def doStandardAction(self, action, userName, **kw):
        if self.state == 'new':
            self.setData(**kw)
            self.doTransition(action)
            self.reindex('state')
            return self
        new = self.createNew(action, userName, **kw)
        new.userName = self.userName
        if self.state == 'running':
            new.replace(self)
        elif self.state in ('planned', 'accepted', 'done'):
            self.state = self.state + '_x'
            self.reindex('state')
        elif self.state in ('finished',) and action == 'cancel':
            self.state = self.state + '_x'
            self.reindex('state')
        new.doTransition(action)
        new.reindex()
        return new

    def modify(self, userName, **kw):
        if self.state == 'new':
            self.setData(**kw)
            return self
        new = self.createNew('modify', userName, **kw)
        new.userName = self.userName
        new.replace(self, keepState=True)
        new.reindex()
        return new

    def delegate(self, userName, **kw):
        if self.state == 'new':
            delegated = self
            self.setData(ignoreParty=True, **kw)
        else:
            if self.state in ('planned', 'accepted', 'delegated', 'moved', 'done'):
                self.state = self.state + '_x'
                self.reindex('state')
            #elif self.state == 'running':
            #    self.doAction('work', userName, 
            #                  end=(kw.get('end') or getTimeStamp()))
            xkw = dict(kw)
            xkw.pop('party', None)
            delegated = self.createNew('delegate', userName, **xkw)
        delegated.state = self.getWorkItemType().delegatedState
        delegated.reindex('state')
        new = delegated.createNew('plan', userName, runId=0, **kw)
        new.data['source'] = delegated.name
        new.doTransition('plan')
        #new.reindex('state')
        new.reindex()
        delegated.data['target'] = new.name
        return new

    def doStart(self, userName, **kw):
        action = 'start'
        # stop any running work item of user:
        # TODO: check: party query OK?
        if (userName == self.userName and 
                self.workItemType in (None, 'work') and 
                self.state != 'running'):
            running = IWorkItems(getParent(self)).query(
                            party=userName, state='running')
            for wi in running:
                if wi.workItemType in (None, 'work'):
                    wi.doAction('work', userName, 
                                end=(kw.get('start') or getTimeStamp()))
        # standard creation of new work item:
        if not kw.get('start'):
            kw['start'] = getTimeStamp()
        kw['end'] = None
        kw['duration'] = kw['effort'] = 0
        return self.doStandardAction(action, userName, **kw)

    def move(self, userName, **kw):
        xkw = dict(kw)
        for k in ('deadline', 'start', 'end'):
            xkw.pop(k, None)    # do not change on source item
        if self.state == 'new': # should this be possible?
            moved = self
            self.setData(kw)
        if self.state in ('done', 'finished', 'running'):
            moved = self        # is this OK? or better new state ..._y?
        else:
            moved = self.createNew('move', userName, **xkw)
            moved.userName = self.userName
        task = kw.pop('task', None)
        new = moved.createNew(None, userName, taskId=task, runId=0, **kw)
        new.userName = self.userName
        new.data['source'] = moved.name
        if self.state == 'new':
            new.state = 'planned'
        else:
            new.state = self.state
        new.reindex()
        moved.data['target'] = new.name
        moved.state = 'moved'
        moved.reindex()
        if self.state in ('planned', 'accepted', 'delegated', 'moved'):
                          #'done', 'finished'):
            self.state = self.state + '_x'
            self.reindex('state')
        #elif self.state in ('done', 'finished'):
        #    self.state = self.state + '_y'
        #    self.reindex('state')
        return new

    def close(self, userName, **kw):
        kw['start'] = kw['end'] = getTimeStamp()
        kw['duration'] = kw['effort'] = None
        new = self.createNew('close', userName, copyData=('title',), **kw)
        new.userName = self.userName
        new.state = 'closed'
        #new.reindex('state')
        new.reindex()
        getParent(self).stopRun(runId=self.runId, finish=True)
        for item in self.currentWorkItems:
            if item.state in ('planned', 'accepted', 'done', 'delegated', 'moved'):
                item.state = item.state + '_x'
                item.reindex('state')
        return new

    specialActions = dict(modify=modify, delegate=delegate, 
                          start=doStart, move=move,
                          close=close)

    def setData(self, ignoreParty=False, **kw):
        if self.state != 'new':
            raise ValueError("Attributes may only be changed in state 'new'.")
        party = kw.pop('party', None)
        if not ignoreParty:
            if party is not None:
                self.userName = party
                self.reindex('userName')
        start = kw.get('start') or kw.get('deadline')   # TODO: check OK?
        if start is not None:
            self.timeStamp = start  # TODO: better use end
            self.reindex('timeStamp')
        data = self.data
        for k, v in kw.items():
            if v is not None:
                data[k] = v
        start, end = data.get('start'), data.get('end')
        if start and end and end < start:
            data['end'] = start

    def createNew(self, action, userName, taskId=None, copyData=None,
                  runId=None, **kw):
        taskId = taskId or self.taskId
        runId = runId is None and self.runId or runId
        if copyData is None:
            copyData = self.initAttributes
        newData = {}
        start = kw.get('start')
        deadline =  kw.get('deadline')
        if not start and deadline:
            kw['start'] = deadline
        for k in self.initAttributes.union(set(['comment'])):
            v = kw.get(k, _not_found)
            if v is _not_found and k in copyData:
                if action == 'start' and k in ('end',):
                    continue
                if action in ('work', 'finish') and k in ('duration', 'effort',):
                    continue
                v = self.data.get(k)
            if v not in (None, _not_found):
                newData[k] = v
        workItems = IWorkItems(getParent(self))
        new = workItems.add(taskId, userName, runId, **newData)
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
