# cybertools.process.execution

""" Execution of a process.
"""

from zope.interface import implementer
from zope.component import adapts
from cybertools.process.interfaces import IActivity, IExecution
from cybertools.process.interfaces import IWorkItem, IActionHandler


@implementer(IExecution)
class Execution(object):

    def __init__(self, parent=None):
        self._currentActivity = None
        self._workItem = None
        self._parent = parent
        self._children = set()

    def getCurrentActivity(self): return self._currentActivity
    def setCurrentActivity(self, activity): self._currentActivity = activity
    currentActivity = property(getCurrentActivity, setCurrentActivity)

    def getWorkItem(self): return self._workItem
    def setWorkItem(self, item): self._workItem = item
    workItem = property(getWorkItem, setWorkItem)

    @property
    def parent(self): return self._parent

    @property
    def children(self): return self._children

    def trigger(self, qualifiers=set()):
        successors = [s for s in self.currentActivity.successors
                        if not qualifiers
                            or qualifiers.union(successor.qualifiers)]
        for successor in successors:
            if len(successors) == 1:
                execution = self
            else:
                execution = Execution(self)
                self.children.add(execution)
            successor.execute(execution)


@implementer(IWorkItem)
class WorkItem(object):

    def __init__(self, execution):
        self._execution = execution
        self._activity = execution.currentActivity

    @property
    def execution(self): return self._execution

    @property
    def activity(self): return self._activity

    _done = False
    @property
    def done(self): return self._done

    def submit(self, data={}):
        _done = True
        self.execution.trigger()


@implementer(IActionHandler)
class WorkActionHandler(object):
    """ A simple action handler that creates a work item.
    """

    adapts(IActivity)

    def __init__(self, context):
        self.context = context

    def handle(self, execution):
        self.workItem = WorkItem(execution)

