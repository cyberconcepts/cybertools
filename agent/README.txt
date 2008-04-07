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

  >>> from cybertools.agent.main import setup
  >>> master = setup(configFile)
  Starting agent application...
  Using controllers base.sample.
  >>> configFile.close()

  >>> master.config
  controller.names = ['base.sample']
  logger.name = 'default'
  logger.standard = 30
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

We schedule a sample job by calling an internal method of the agent's
controller. In addition to the output of the job execution itself we
also get a note from the controller about the feedback it received
about the outcome of the job execution.

  >>> master.controllers[0].enterJob('sample', 'sample01')
  Job 00001 on agent sample01 has been executed.
  Job 00001 completed; result: None;

Logging
-------

  >>> master.logger
  <cybertools.agent.base.log.Logger object ...>
  >>> agent01.logger is master.logger
  True

  >>> master.config.logger.standard = 20
  >>> master.logger.setup()
  >>> master.controllers[0].enterJob('sample', 'sample01')
  Job 00002 on agent sample01 has been executed.
  2... agent:sample01 job:00002 message:job execution result:OK
  Job 00002 completed; result: None;

  >>> for r in master.logger.records:
  ...     print r
  2... agent:sample01 job:00001 message:job execution result:OK
  2... agent:sample01 job:00002 message:job execution result:OK


Using the Twisted-based Scheduler
=================================

By specifying the core scheduler in the agent's configuration this will be
used automatically for scheduling.

In addition, we use another sample controller, now also the twisted-based
from the core package. This will in turn set up a queueable agent from
the core package so that now everything is running under the control of
the twisted reactor.

  >>> config = '''
  ... controller(names=['core.sample'])
  ... scheduler(name='core')
  ... logger(name='default', standard=30)
  ... '''
  >>> master = setup(config)
  Starting agent application...
  Using controllers core.sample.

  >>> master.scheduler
  <cybertools.agent.core.schedule.Scheduler object ...>

We enter the same job specification as above.

  >>> master.controllers[0].enterJob('sample', 'sample01')

Now the job is not executed immediately - we have to hand over control to
the twisted reactor first. The running of the reactor is simulated by
the ``iterate()`` method provided for testing.

  >>> from cybertools.agent.tests import tester
  >>> tester.iterate()
  Job 00001 on agent sample01 has been executed.
  Job 00001 completed; result: Done;
