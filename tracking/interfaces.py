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
Interface definitions for tracking of user interactions.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema


# user interaction tracking

class IRun(Interface):
    """ A set of interactions, sort of a session.
    """

    id = Attribute('A unique integer that identifies a run within a tracking storage')
    start = Attribute('Timestamp of run creation')
    end = Attribute('Timestamp of last interaction or of stopping the run')
    finished = Attribute('Boolean that is set to True if run was finished explicitly')


class ITrack(Interface):
    """ Result data from the interactions of a user with an task.
    """

    data = Attribute('The data for this track, typically a mapping')
    metadata = Attribute('A mapping with the track\'s metadata')
    indexdata = Attribute('A mapping with the data to be used for indexing')


class ITrackingStorage(Interface):
    """ A utility for storing user tracks.
    """

    def startRun(taskId=None):
        """ Create a new run and return its id.
            If a taskId is given, record the runId as the tasks current run.
        """

    def stopRun(taskId=None, runId=0, finish=True):
        """ Stop/finish a run.
            If the runId is 0 use the task's current run.
            If the run is the task's current one remove it from the set
            of current runs.
            Set the run's ``finished`` flag to the value of the ``finish``
            argument.
            Return the real runId; return 0 if there is no run for the
            parameters given.
        """

    def getRun(taskId=None, runId=0):
        """ Return the run object identified by ``runId``. Return None
            if there is no corresponding run.
            If ``runId`` is 0 and a ``taskId`` is given return the
            current run of the task.
        """

    def saveUserTrack(taskId, runId, userName, data, update=False):
        """ Save the data given (typically a mapping object) to the user track
            corresponding to the user name, task id, and run id given.
            If the runId is 0 use the task's current run.
            If the ``update`` flag is set, the new track updates the last
            one for the given set of keys.
            Return the new track item's id.
        """

    def query(**criteria):
        """ Search for tracks. Possible criteria are: taskId, runId,
            userName, timeFrom, timeTo.
        """

    def getUserTracks(taskId, runId, userName):
        """ Return the user tracks corresponding to the user name and
            task id given. If a 0 run id is given use the current one.
        """

    def getLastUserTrack(taskId, runId, userName):
        """ Return the last user track (that with the highest timestamp value)
            corresponding to the user name and task id given.
            If a 0 run id is given use the current one.
        """

    def getUserNames(taskId):
        """ Return all user names (user ids) that have tracks for the
            task given.
        """

    def getTaskIds():
        """ Return all ids of the tasks for which there are any tracks.
        """

    def reindexTracks():
        """ Reindexes all tracks - in case of trouble...
        """

