================================================
Agents for Job Execution and Communication Tasks
================================================

Agents collect informations and transfer them e.g. to a loops server.

  ($Id$)

This package does not depend on zope or the other loops packages
but represents a standalone application.

But we need a reactor for working with Twisted; in order not to block
testing when running the reactor we use reactor.iterate() calls
wrapped in a ``tester`` object.

  >>> from cybertools.agent.tests import tester


Master Agent
============

The agent uses Twisted's cooperative multitasking model.

This means that all calls to services (like crawler, transporter, ...)
return a deferred that must be supplied with a callback method (and in
most cases also an errback method).

  >>> #from cybertools.agent.core.agent import Master
  >>> #master = Master()


