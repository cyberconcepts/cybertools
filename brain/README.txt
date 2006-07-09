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
  >>> n01.state.value
  1.0
  >>> n02.state.value
  1.0

When we trigger a neuron, all its receivers get triggered so that the
receivers' state is updated:

  >>> n01.trigger()
  >>> n01.state.value
  1.0
  >>> n02.state.value
  2.0

