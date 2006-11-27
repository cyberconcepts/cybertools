#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
BTree-based implementation of user tracking.

$Id$
"""

import time

from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from zope.index.field import FieldIndex

from persistent import Persistent
from BTrees import OOBTree
from BTrees.IFBTree import intersection

from interfaces import ITrackingStorage, ITrack


class TrackingStorage(BTreeContainer):

    implements(ITrackingStorage)

    trackNum = runId = 0

    indexAttributes = ('taskId', 'runId', 'userName', 'timeStamp')

    def __init__(self, *args, **kw):
        super(TrackingStorage, self).__init__(*args, **kw)
        self.indexes = OOBTree.OOBTree()
        for idx in self.indexAttributes:
            self.indexes[idx] = FieldIndex()
        self.currentRuns = OOBTree.OOBTree()
        self.taskUsers = OOBTree.OOBTree()

    def idFromNum(self, num):
        return '%07i' % (num)

    def startRun(self, taskId):
        self.runId += 1
        self.currentRuns[taskId] = self.runId
        return self.runId

    def stopRun(self, taskId):
        runId = self.currentRuns.get(taskId)
        if runId:
            del self.currentRuns[taskId]
        return runId

    def saveUserTrack(self, taskId, runId, userName, data, replace=False):
        if not runId:
            runId = self.currentRuns.get(taskId) or self.startRun(taskId)
        trackNum = 0
        if replace:
            track = self.getLastUserTrack(taskId, runId, userName)
            if track:
                trackId = str(track.__name__)
                trackNum = int(trackId)
                del self[trackId]
        if not trackNum:
            self.trackNum += 1
            trackNum = self.trackNum
            trackId = self.idFromNum(trackNum)
        timeStamp = int(time.time())
        track = Track(taskId, runId, userName, timeStamp, data)
        self[trackId] = track
        self.indexTrack(trackNum, track)
        return trackId

    def indexTrack(self, trackNum, track):
        md = track.metadata
        for attr in self.indexAttributes:
            self.indexes[attr].index_doc(trackNum, md[attr])
        taskId = md['taskId']
        userName = md['userName']
        if taskId not in self.taskUsers:
            self.taskUsers[taskId] = OOBTree.OOTreeSet()
        self.taskUsers[taskId].update([userName])

    def reindexTracks(self):
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
        else: return None

    def query(self, **kw):
        result = None
        for idx in kw:
            value = kw[idx]
            if idx in self.indexAttributes:
                result = self.intersect(result, self.indexes[idx].apply((value, value)))
            elif idx == 'timeFrom':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((value, None)))
            elif idx == 'timeTo':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((None, value)))
        return result and [self[self.idFromNum(r)] for r in result] or set()

    def intersect(self, r1, r2):
        return r1 is None and r2 or intersection(r1, r2)

    def getUserNames(self, taskId):
        return sorted(self.taskUsers.get(taskId, []))

    def getTaskIds(self):
        return self.taskUsers.keys()


class Track(Persistent):

    implements(ITrack)

    metadata_attributes = ('taskId', 'runId', 'userName', 'timeStamp')

    @property
    def metadata(self):
        return dict((attr, getattr(self, attr)) for attr in self.metadata_attributes)

    def __init__(self, taskId, runId, userName, timeStamp, data={}):
        self.taskId = taskId
        self.runId = runId
        self.userName = userName
        self.timeStamp = timeStamp
        self.data = data

    def __repr__(self):
        md = self.metadata
        md['timeStamp'] = timeStamp2ISO(md['timeStamp'])
        return '<Track %s: %s>' % (`[md[a] for a in self.metadata_attributes]`,
                                     `self.data`)

def timeStamp2ISO(ts):
    return time.strftime('%Y-%m-%d %H:%M', time.gmtime(ts))

