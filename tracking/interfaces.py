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
loops tracking interface definitions.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema


# user interaction tracking

class ITrack(Interface):
    """ Result data from the interactions of a user with an task.
    """

    data = Attribute('The data for this track, typically a mapping')
    metadata = Attribute('A mapping with the track\'s metadata')


class ITrackingStorage(Interface):
    """ A utility for storing user tracks.
    """

    def startRun(taskId):
        """ Creates a new run for the task given and return its id.
        """

    def stopRun(taskId):
        """ Remove the current run entry for the task given.
        """

    def saveUserTrack(taskId, runId, userName, data):
        """ Save the data given (typically a mapping object) to the user track
            corresponding to the user name, task id, and run id given.
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

