================================================
Agents for Job Execution and Communication Tasks
================================================

Agents collect informations and transfer them e.g. to a loops server.

  ($Id: README.txt 2413 2008-02-23 14:07:15Z helmutm $)

This package does not depend on zope or the other loops packages
but represents a standalone application.

But we need a reactor for working with Twisted; in order not to block
testing when running the reactor we use reactor.iterate() calls
wrapped in a ``tester`` object.

  >>> from cybertools.agent.tests import tester


Crawler
============

The agent uses Twisted's cooperative multitasking model.

Crawler is the base class for all derived Crawlers like the filesystem crawler
and the mailcrawler. The SampleCrawler returns a deferred that already had a
callback being called, so it will return at once.
Returns a deferred that must be supplied with a callback method (and in
most cases also an errback method).

  >>> from cybertools.agent.crawl.base import SampleCrawler
  >>> from twisted.internet import defer
  >>> crawler = SampleCrawler()
  >>> deferred = crawler.collect()
  SampleCrawler is collecting.


