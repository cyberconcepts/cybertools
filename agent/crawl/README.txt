================================================
Agents for Job Execution and Communication Tasks
================================================

  ($Id$)

  >>> from cybertools.agent.base.agent import Master

  >>> config = '''
  ... controller(name='core.sample')
  ... scheduler(name='core')
  ... logger(name='default', standard=30)
  ... '''
  >>> master = Master(config)
  >>> master.setup()


Crawler
=======

The agent uses Twisted's cooperative multitasking model.

Crawler is the base class for all derived crawlers like the filesystem crawler
and the mailcrawler. The SampleCrawler returns a deferred that already had a
callback being called, so it will return at once.

Returns a deferred that must be supplied with a callback method (and in
most cases also an errback method).

We create the sample crawler via the master's controller. The sample
controller provides a simple method for this purpose.

  >>> controller = master.controllers[0]
  >>> controller.createAgent('crawl.sample', 'crawler01')

In the next step we request the start of a job, again via the controller.

  >>> controller.enterJob('sample', 'crawler01')

The job is not executed immediately - we have to hand over control to
the twisted reactor first.

  >>> from cybertools.agent.tests import tester
  >>> tester.iterate()
  SampleCrawler is collecting.
  Job 00001 completed; result: [];
