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
    Generic interfaces, ``tests`` module, this ``README.txt`` file.

base
    Base and sample classes

core
    Agent and scheduling implementations.

control
    Communication with an external agent control and job database application

crawl
    Scanning/crawling some system, e.g. the database of an email application,
    the local file system, or an external document source

transport
    Transfer of information objects to agents on another machine or
    to an information management application (e.g. loops)

util
    Various utility modules, e.g. a backport of the
    ``twisted.internet.task.coiterate()`` function from Twisted 2.5.

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

The code resides in in the ``base`` sub-package.

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
  logger.name = 'sample'
  scheduler.name = 'sample'

Controller
----------

Creation of agents and scheduling of jobs is controlled by the controller
object. This is typically associated with a sort of control storage that
provides agent and job specifications and receives the results of job
execution.

We open the controller and read in the specifications via the master agent's
``setup`` method.

  >>> master.setup()

Other Agents
------------

Job Scheduling and Execution
----------------------------
