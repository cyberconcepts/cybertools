=============================================================
A proof-of-concept Project Aiming at a sort of Neural Network
=============================================================

  ($Id$)

Let's start with creating a few neurons and connecting them with synapses.

  >>> from cybertools.brain.neuron import Neuron, Synapsis
  >>> n01 = Neuron()
  >>> n02 = Neuron()

In the simple default implementation the neurons are connected automatically
when creating a synapsis:

  >>> s0102 = Synapsis(n01, n02)
  >>> n01.senders
  []
  >>> n01.receivers == [s0102]
  True
  >>> n01.getState()
  <State 0.0>
  >>> n02.getState()
  <State 0.0>

When we change the state of a neuron and notify it, all its receiver synapses
get triggered so that the receiver neurons' states are updated:

  >>> from cybertools.brain.state import State
  >>> n01.setState(State(1.0))
  >>> n01.getState()
  <State 1.0>
  >>> n01.notify()
  >>> n02.getState()
  <State 1.0>

To allow for concurrent access to the brain by different clients
simultaneously, the changes to the neurons' states may be under the control of
a session:

  >>> n01.setState(State())
  >>> n02.setState(State())
  >>> from cybertools.brain.session import Session
  >>> session = Session()
  >>> n01.setState(State(1.0), session)
  >>> n01.getState()
  <State 0.0>
  >>> n01.getState(session)
  <State 1.0>
  >>> n01.notify(session)
  >>> n02.getState()
  <State 0.0>
  >>> n02.getState(session)
  <State 1.0>
