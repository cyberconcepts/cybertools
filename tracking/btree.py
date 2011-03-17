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
ZODB-/BTree-based implementation of user interaction tracking.

$Id$
"""

import time
from persistent import Persistent
from BTrees import OOBTree, IOBTree
from BTrees.IFBTree import intersection, union
from zope.component import adapter
from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.index.field import FieldIndex
from zope.traversing.api import getParent
from zope.traversing.interfaces import IPhysicallyLocatable

from cybertools.tracking.interfaces import IRun, ITrackingStorage, ITrack
from cybertools.util.date import getTimeStamp, timeStamp2ISO


class Run(object):

    implements(IRun)

    id = start = end = 0
    finished = False

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Run %s>' % ', '.join((str(self.id),
                                       timeStamp2ISO(self.start),
                                       timeStamp2ISO(self.end),
                                       str(self.finished)))


class Track(Persistent):

    #implements(ITrack, IPhysicallyLocatable)
    implements(ITrack)

    metadata_attributes = ('taskId', 'runId', 'userName', 'timeStamp')
    index_attributes = metadata_attributes
    typeName = 'Track'

    @property
    def metadata(self):
        return dict((attr, getattr(self, attr)) for attr in self.metadata_attributes)

    indexdata = metadata

    def __init__(self, taskId, runId, userName, data=None):
        self.taskId = taskId
        self.runId = runId
        self.userName = userName
        self.timeStamp = getTimeStamp()
        if data is None:
            data = {}
        self.data = data

    #def getName(self):
    #    return self.__name__

    def update(self, newData):
        if not newData:
            return
        self.timeStamp = getTimeStamp()
        getParent(self).indexTrack(0, self, 'timeStamp')
        data = self.data
        data.update(newData)
        self.data = data    # record change

    def __repr__(self):
        md = self.metadata
        md['timeStamp'] = timeStamp2ISO(md['timeStamp'])
        return '<%s %s: %s>' % (self.typeName,
                                repr([md[a] for a in self.metadata_attributes]),
                                repr(self.data))

    @property
    def name(self):
        return self.__name__


class TrackingStorage(BTreeContainer):

    implements(ITrackingStorage)

    trackFactory = Track
    indexAttributes = trackFactory.index_attributes

    trackNum = runId = 0
    runs = None             # currently active runs
    finishedRuns = None     # finished runs
    currentRuns = None      # the currently active run for each task

    def __init__(self, *args, **kw):
        trackFactory = kw.pop('trackFactory', None)
        if trackFactory is not None:
            self.trackFactory = trackFactory
            self.indexAttributes = trackFactory.index_attributes
        super(TrackingStorage, self).__init__(*args, **kw)
        self.indexes = OOBTree.OOBTree()
        for idx in self.indexAttributes:
            self.indexes[idx] = FieldIndex()
        self.runs = IOBTree.IOBTree()
        self.finishedRuns = IOBTree.IOBTree()
        self.currentRuns = OOBTree.OOBTree()
        self.taskUsers = OOBTree.OOBTree()

    def setupIndexes(self):
        changed = False
        for idx in self.indexAttributes:
            if idx not in self.indexes:
                self.indexes[idx] = FieldIndex()
                changed = True
        if changed:
            self.reindexTracks()

    def idFromNum(self, num):
        return '%07i' % (num)

    def startRun(self, taskId=None):
        self.runId += 1
        runId = self.runId
        if taskId is not None:
            self.currentRuns[taskId] = runId
        run = self.runs[runId] = Run(runId)
        run.start = run.end = getTimeStamp()
        return runId

    def stopRun(self, taskId=None, runId=0, finish=True):
        if taskId is not None:
            currentRun = self.currentRuns.get(taskId)
            runId = runId or currentRun
            if runId and runId == currentRun:
                del self.currentRuns[taskId]
        run = self.getRun(runId=runId)
        if run is not None:
            run.end = getTimeStamp()
            run.finished = finish
            if finish:
                self.moveToFinishedRuns(run)
            return runId
        return 0

    def moveToFinishedRuns(self, run):
        id = run.id
        if id in self.runs:
            del self.runs[id]
        if self.finishedRuns is None:   # backward compatibility
            self.finishedRuns = IOBTree.IOBTree()
        self.finishedRuns[id] = run

    def getRun(self, taskId=None, runId=0):
        if self.runs is None:
            self.runs = IOBTree.IOBTree()
        if taskId and not runId:
            runId = self.currentRuns.get(taskId)
        if runId:
            return self.runs.get(runId) or self.finishedRuns.get(runId)
        return None

    def generateTrackId(self):
        self.trackNum += 1
        trackId = self.idFromNum(self.trackNum)
        return trackId, self.trackNum

    def saveUserTrack(self, taskId, runId, userName, data, update=False,
                      timeStamp=None):
        ts = timeStamp or getTimeStamp()
        if not runId:
            runId = self.currentRuns.get(taskId) or self.startRun(taskId)
        run = self.getRun(runId=runId)
        if run is None:
            raise ValueError('Invalid run: %i.' % runId)
        if run.end < ts:
            run.end = ts
        if update:
            track = self.getLastUserTrack(taskId, runId, userName)
            if track is not None:
                return self.updateTrack(track, data)
        trackId, trackNum = self.generateTrackId()
        track = self.trackFactory(taskId, runId, userName, data)
        track.__parent__ = self
        track.__name__ = trackId
        if timeStamp:
            track.timeStamp = timeStamp
        self[trackId] = track
        self.indexTrack(trackNum, track)
        return trackId

    def updateTrack(self, track, data):
        trackId = str(track.__name__)
        trackNum = int(trackId)
        track.update(data)
        self.indexTrack(trackNum, track)
        return trackId

    def removeTrack(self, track):
        trackId = str(track.__name__)
        trackNum = int(trackId)
        if trackId in self:
            del self[trackId]
        self.unindexTrack(trackNum, track)

    def indexTrack(self, trackNum, track, idx=None):
        if not trackNum:
            trackNum = int(track.__name__)
        data = track.indexdata
        if idx is not None:
            if idx not in self.indexAttributes:
                raise ValueError("Index '%s' not available." % (idx))
            return self.indexes[idx].index_doc(trackNum, data[idx])
        for attr in self.indexAttributes:
            value = data[attr]
            if value is None:
                self.indexes[attr].unindex_doc(trackNum)
            else:
                self.indexes[attr].index_doc(trackNum, value)
        taskId = data['taskId']
        userName = data['userName']
        if taskId not in self.taskUsers:
            self.taskUsers[taskId] = OOBTree.OOTreeSet()
        self.taskUsers[taskId].update([userName])

    def unindexTrack(self, trackNum, track):
        for attr in self.indexAttributes:
            self.indexes[attr].unindex_doc(trackNum)

    def reindexTracks(self):
        for attr in self.trackFactory.index_attributes:
            self.indexes[attr].clear()
        for trackId in self:
            trackNum = int(trackId)
            self.indexTrack(trackNum, self[trackId])

    def getUserTracks(self, taskId, runId, userName):
        if not runId:
            runId = self.currentRuns.get(taskId)
        return self.query(taskId=taskId, runId=runId, userName=userName)

    def getLastUserTrack(self, taskId, runId, userName):
        tracks = self.getUserTracks(taskId, runId, userName)
        if tracks:
            return sorted(tracks, key=lambda x: x.timeStamp)[-1]
        else:
            return None

    def query(self, **kw):
        result = None
        for idx in kw:
            value = kw[idx]
            if idx in self.indexAttributes:
                if type(value) not in (list, tuple):
                    value = [value]
                resultx = None
                for v in value:
                    resultx = self.union(resultx, self.indexes[idx].apply((v, v)))
                result = self.intersect(result, resultx)
            elif idx == 'timeFrom':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((value, None)))
            elif idx == 'timeTo':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((None, value)))
            elif idx == 'timeFromTo':  # expects a tuple (from, to)
                start, end = value
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((start, end)))
        result = result and (self.get(self.idFromNum(r)) for r in result) or set()
        #return result
        return [t for t in result if t is not None]

    def intersect(self, r1, r2):
        return r1 is None and r2 or intersection(r1, r2)

    def union(self, r1, r2):
        return r1 is None and r2 or union(r1, r2)

    def getUserNames(self, taskId):
        return sorted(self.taskUsers.get(taskId, []))

    def getTaskIds(self):
        return self.taskUsers.keys()


@adapter(ITrack, IObjectRemovedEvent)
def unindexTrack(context, event):
    getParent(context).unindexTrack(int(context.__name__), context)
