================================================
Agents for Job Execution and Communication Tasks
================================================

Agents do some work specified by a jobs, the main task being to collect
information objects from the local machine or some external source and
transfer them e.g. to a loops server on the same machine or another.


  ($Id$)

This package does not depend on Zope but represents a standalone application.


Sub-Packages
============

Top-level
    Generic interfaces, ``commponents``: adapter registry,
    ``tests`` module, this ``README.txt`` file.

base
    Base and sample classes.

core
    Agent and scheduling implementations.

control
    Communication with an external agent control and job database application.

crawl
    Scanning/crawling some system, e.g. the database of an email application,
    the local file system, or an external document source.

transport
    Transfer of information objects to agents on another machine or
    to an information management application (e.g. loops).

util
    Various utility modules, e.g. a backport of the
    ``twisted.internet.task.coiterate()`` function from Twisted 2.5 so that
    we can use the Twisted version coming with Zope 3.3.1 for
    cybertools.agent.

All sub-packages except ``base`` depend on Twisted.


Object Structure and Control Flow
=================================

::

                ----------       ------------
  --------     |          |<---1|            |
 | config |--> |  master  |<---2| controller |
  --------    /|          |4--->|            |
             /  ----------       ------------
            /     1  ^  2
           /      |  |   \       -----------
          /       |  |    `---->| scheduler |
         v        v  4           -----------
      -----     ---------             3
     | log |<--|  agent  |<----------´
      -----     ---------

(1) Agent specifications control creation and setup of agents

(2) Job specifications control scheduling of jobs

(3) Scheduler triggers job execution by agent

(4) Results are recorded, possibly triggering further actions


Basic Stuff
===========

While the real application is based on the asynchronous communication
framework Twisted there is some basic stuff (mainly interfaces and
base classes with basic, sample, or dummy implementations) that is
independent of Twisted.

The code for this resides in in the ``base`` sub-package.

Master Agent and Configuration
------------------------------

All activity is controlled by the master agent.

The master agent is set up according to the specifications in a
configuration file.

The configuration typically provides only basic informations, e.g. about
the controller(s) and logger(s) to be used; details on jobs and agent
configuration are provided by the controller.

  >>> from cybertools.agent.tests import baseDir
  >>> import os
  >>> configFile = open(os.path.join(baseDir, 'base', 'sample.cfg'))

So we are now ready to create a master agent and configure it by supplying
the path to the configuration file.

  >>> from cybertools.agent.base.agent import Master
  >>> master = Master(configFile)

  >>> master.config
  controller.name = 'sample'
  logger.name = 'default'
  logger.standard = 20
  scheduler.name = 'sample'

Controllers
-----------

Creation of agents and scheduling of jobs is controlled by controller
objects. These are typically associated with a sort of control storage that
provides agent and job specifications and receives the results of job
execution.

  >>> master.controllers
  [<cybertools.agent.base.control.SampleController object ...>]

We make the contollers provide the specifications via the master agent's
``setup()`` method.

  >>> master.setup()

Other Agents
------------

The above ``setup()`` call has triggered the creation of one child agent -
that is all the sample controller provides.

  >>> master.children
  {'sample01': <cybertools.agent.base.agent.SampleAgent object ...>}

Let's check a few attributes of the newly created agent.

  >>> agent01 = master.children['sample01']
  >>> agent01.master is master
  True
  >>> agent01.config is master.config
  True

Job Scheduling and Execution
----------------------------

A scheduler is responsible for triggering the execution of a job at the
appropriate time. The master agent schedules the jobs based upon the
information (job specifications) it gets from the controller. There
is just one scheduler associated with the master agent.

  >>> master.scheduler
  <cybertools.agent.base.schedule.Scheduler object ...>

We schedule a sample job by taking the role of the controller and simply
call the master agent's callback method for entering jobs.

  >>> from cybertools.agent.base.control import JobSpecification
  >>> jobSpec = JobSpecification('sample', agent='sample01')
  >>> master.setupJobs([jobSpec])
  Job <...Job object ...> on agent <...SampleAgent object ...> has been executed.

Logging
-------

  >>> master.logger
  <cybertools.agent.base.log.Logger object ...>
  >>> agent01.logger is master.logger
  True
