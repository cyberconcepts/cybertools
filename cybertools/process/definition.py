# cybertools.process.definition

""" Process definitions.
"""

from zope import component
from zope.interface import implementer
from cybertools.process.interfaces import IActivity, IProcess
from cybertools.process.interfaces import IActionHandler
from cybertools.process.execution import Execution


@implementer(IActivity)
class Activity(object):

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


@implementer(IProcess)
class Process(object):

    def __init__(self):
        self._startActivity = Activity()

    @property
    def startActivity(self): return self._startActivity

    def execute(self):
        return self.startActivity.execute()
