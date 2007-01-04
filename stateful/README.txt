================
Stateful objects
================

  ($Id$)

  >>> from cybertools.stateful.definition import StatesDefinition
  >>> from cybertools.stateful.definition import State, Transition
  >>> from cybertools.stateful.base import Stateful

  >>> class Demo(Stateful):
  ...     pass

  >>> demo = Demo()
  >>> demo.getState()
  'started'
