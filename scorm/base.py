#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Base classes for providing a generic SCORM-compliant API.

$Id$
"""

from zope import interface
from zope.interface import implements

from cybertools.scorm.interfaces import IScormAPI
from cybertools.tracking.btree import TrackingStorage


OK = '0'


class ScormAPI(object):
    """ ScormAPI objects are temporary adapters created by
        browser or XML-RPC views.
    """

    implements(IScormAPI)

    def __init__(self, storage, taskId, runId, userId):
        self.taskId = taskId
        self.runId = runId
        self.userId = userId
        self.storage = storage

    def initialize(self, parameter=''):
        # Note that the run has already been started upon SCO launch, the runId
        # usually being part of the URI or XML-RPC call arguments.
        return OK

    def terminate(self, parameter=''):
        rc = self.commit()
        if rc == OK:
            self.storage.stopRun(self.taskId, self.runId)
        return rc

    def commit(self, parameter=''):
        return OK

    def setValue(self, element, value):
        tracks = self.storage.getUserTracks(self.taskId, self.runId, self.userId)
        prefix, key = self._splitKey(element)
        data = self._getTrackData(tracks, prefix) or {}
        update = bool(data)
        data['key_prefix'] = prefix
        data.update({key: value})
        self.storage.saveUserTrack(self.taskId, self.runId, self.userId, data,
                                   update=update)
        return OK

    def setValues(self, mapping={}, **kw):
        mapping.update(kw)
        # TODO: optimize, i.e. retrieve existing tracks only once.
        for key, value in mapping:
            rc = self.setValue(key, value)
            if rc != OK:
                return rc
        return OK

    def getValue(self, element):
        tracks = self.storage.getUserTracks(self.taskId, self.runId, self.userId)
        prefix, key = self._splitKey(element)
        data = self._getTrackData(tracks, prefix) or {}
        if key in data:
            return data[key], OK
        else:
            return '', '403'

    def getErrorString(self, errorCode):
        return ''

    def getDiagnostic(self, code):
        return ''

    # helper methods

    def _splitKey(self, element):
        if element.startswith('cmi.interactions.'):
            parts = element.split('.')
            return '.'.join(parts[:3]), '.'.join(parts[3:])
        return '', element

    def _getTrackData(self, tracks, prefix):
        track = None
        for tr in reversed(sorted(tracks, key=lambda x: x.timeStamp)):
            if tr and tr.data.get('key_prefix', None) == prefix:
                return tr.data
        return {}
