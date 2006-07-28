Business Process Management
===========================

  ($Id$)

We start with the definition of a simple process:

  startNode --> n01 --> endNode

  >>> from cybertools.process.definition import ProcessDefinition, Node, Transition
  >>> process = ProcessDefinition()
  >>> n01 = Node()
  >>> process.startNode.addTransition(n01)
  >>> n01.addTransition(process.endNode)

Now let's execute the process:

  >>> from cybertools.process.execution import ProcessInstance
  >>> instance = ProcessInstance(process)
  >>> execution = instance.execute()

As there aren't any interactions with the outside world in our process we
don't see anything. But we can check if the process instance has reached the
process' end node:

  >>> execution.currentNode is process.endNode
  True

So let's now associate an action handler with the process' nodes:

  >>> from zope.component import provideAdapter, adapts
  >>> from zope.interface import implements
  >>> from cybertools.process.interfaces import INode, IActionHandler

  >>> class DummyHandler(object):
  ...     implements(IActionHandler)
  ...     adapts(INode)
  ...     def __init__(self, context): pass
  ...     def handle(self, execution):
  ...         print 'working.'

  >>> provideAdapter(DummyHandler)
  >>> execution = instance.execute()
  working.
  >>> execution.currentNode is process.startNode
  True
  >>> execution.trigger()
  working.
  >>> execution.currentNode is n01
  True
  >>> execution.trigger()
  working.
  >>> execution.currentNode is process.endNode
  True
