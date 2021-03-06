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
Process definitions.

$Id$
"""

from zope import component
from zope.interface import implements
from cybertools.process.interfaces import IActivity, IProcess
from cybertools.process.interfaces import IActionHandler
from cybertools.process.execution import Execution


class Activity(object):

    implements(IActivity)

    def __init__(self, name=u'', title=u'', handlerName=''):
        self._successors = set()
        self._handlerName = handlerName
        self.__name__ = name
        self.title = title

    @property
    def successors(self): return self._successors

    def getHandlerName(self): return self._handlerName
    def setHandlerName(self, name): self._handlerName = name
    handlerName = property(getHandlerName, setHandlerName)

    def add(self, activity):
        self.successors.add(activity)

    def execute(self, execution=None):
        if execution is None:
            execution = Execution()
        execution.currentActivity = self
        handler = component.queryAdapter(self, IActionHandler, name=self.handlerName)
        if handler is not None:
            handler.handle(execution) # creates work item; work item triggers execution
        else:
            execution.trigger()
        return execution


class Process(object):

    implements(IProcess)

    def __init__(self):
        self._startActivity = Activity()

    @property
    def startActivity(self): return self._startActivity

    def execute(self):
        return self.startActivity.execute()
