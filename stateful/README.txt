================
Stateful Objects
================

  ($Id$)

  >>> from cybertools.stateful.definition import StatesDefinition
  >>> from cybertools.stateful.definition import State, Transition
  >>> from cybertools.stateful.definition import registerStatesDefinition
  >>> from cybertools.stateful.base import Stateful

We start with a simple demonstration class that provides stateful
behaviour directly.

  >>> class Demo(Stateful):
  ...     pass

  >>> demo = Demo()

The default states definition has the `started` state as its initial
state.

  >>> demo.getState()
  'started'
  >>> demo.getStateObject().title
  'Started'

We can now execute the `finish` Transition.

  >>> demo.doTransition('finish')
  >>> demo.getState()
  'finished'

More complex states definitions
-------------------------------

We'll use a predefined simple publishing workflow that.

  >>> from cybertools.stateful.publishing import simplePublishing
  >>> registerStatesDefinition(simplePublishing())

  >>> demo = Demo()
  >>> demo.statesDefinition = 'publishing'
  >>> demo.getState()
  'draft'

  >>> [t.title for t in demo.getAvailableTransitions()]
  ['publish', 'hide', 'archive', 'remove']

If we try to execute a transition that is not an outgoing transition
of the current state we get an error.

  >>> demo.doTransition('retract')
  Traceback (most recent call last):
  ...
  ValueError: Transition 'retract' is not reachable from state 'draft'.
  >>> demo.getState()
  'draft'


Stateful Adapters
=================

Objects that show stateful behaviour need not be derived from the Stateful
class, for persistent objects one can also provide a stateful adapter.

  >>> from persistent import Persistent
  >>> class Demo(Persistent):
  ...     pass

  >>> demo = Demo()

  >>> from zope import component
  >>> from cybertools.stateful.base import StatefulAdapter
  >>> component.provideAdapter(StatefulAdapter)

We can now retrieve a stateful adapter using the IStateful interface.

  >>> from cybertools.stateful.interfaces import IStateful

  >>> statefulDemo = IStateful(demo)
  >>> statefulDemo.getState()
  'started'
  >>> statefulDemo.getStateObject().title
  'Started'

  >>> statefulDemo.doTransition('finish')
  >>> statefulDemo.getState()
  'finished'

If we make a new adapter for the same persistent object we get
back the state that is stored with the object.

  >>> statefulDemo = IStateful(demo)
  >>> statefulDemo.getState()
  'finished'
