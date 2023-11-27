Business Process Management
===========================

  ($Id$)

We start with the definition of a simple process:

  startActivity --> n01 --> endActivity

  >>> from cybertools.process.definition import Process, Activity
  >>> process = Process()
  >>> n01 = Activity()
  >>> process.startActivity.add(n01)
  >>> n02 = Activity()
  >>> n01.add(n02)

Now let's execute the process:

  >>> execution = process.execute()

As there aren't any interactions with the outside world in our process we
don't see anything. But we can check if the process instance has reached the
process' end activity:

  >>> execution.currentActivity is n02
  True

So let's now associate an action handler with the process' activitys:

  >>> from zope.component import provideAdapter, adapts
  >>> from zope.interface import implements
  >>> from cybertools.process.interfaces import IActivity, IActionHandler

  >>> class DummyHandler(object):
  ...     implements(IActionHandler)
  ...     adapts(IActivity)
  ...     def __init__(self, context): pass
  ...     def handle(self, execution):
  ...         print 'working.'

  >>> provideAdapter(DummyHandler)
  >>> execution = process.execute()
  working.
  >>> execution.currentActivity is process.startActivity
  True
  >>> execution.trigger()
  working.
  >>> execution.currentActivity is n01
  True
  >>> execution.trigger()
  working.
  >>> execution.currentActivity is n02
  True

Next we'll use a predefined action handler that creates a work item. As this
makes only sense if the action handler can give the outside world access
to the work item somehow, we have to subclass this generic, abstract class:

  >>> workItems = []
  >>> from cybertools.process.execution import WorkActionHandler
  >>> class MyActionHandler(WorkActionHandler):
  ...     def handle(self, execution):
  ...         super(MyActionHandler, self).handle(execution)
  ...         workItems.append(self.workItem)
  >>> provideAdapter(MyActionHandler)

  >>> execution = process.execute()

Now the process is waiting for somebody to pick up the work item and
submit it:

  >>> execution.currentActivity is process.startActivity
  True
  >>> workItem = workItems[0]
  >>> workItem.done
  False
  >>> workItem.submit()
  >>> execution.currentActivity is n01
  True
  >>> workItem.done
  False


