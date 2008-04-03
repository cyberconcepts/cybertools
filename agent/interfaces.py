#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
cybertools agent interfaces.

$Id$
"""

from zope.interface import Interface, Attribute

from cybertools.util.jeep import Jeep


# agents

class IAgent(Interface):
    """ An agent waits for jobs to execute.
    """

    name = Attribute('A name identifying the agent.')
    master = Attribute('IMaster instance.')
    config = Attribute('Configuration settings.')
    logger = Attribute('Logger instance to be used for recording '
                    'job execution and execution results.')

    def send(job):
        """ If the agent supports queueing and the agent is busy put
            job in queue, otherwise just execute the job.
        """

    def execute(job):
        """ Execute a job using the parameters given.
        """


class IQueueableAgent(Interface):
    """ An agent that keeps a queue of jobs. A queueable agent
        executes not more than one job at a time; when a running
        job is finished the next one will be taken from the queue.
    """

    queue = Attribute('A sequence of jobs to execute.')

    def process():
        """ Do the real work asynchronously, returning a deferred.
            This method will be called by execute().
        """


class IMaster(IAgent):
    """ The top-level controller agent.
    """

    config = Attribute('Central configuration settings.')
    controllers = Attribute('Collection of IController instances.')
    scheduler = Attribute('IScheduler instance.')
    children = Attribute('A collection of agents that are managed by this '
                    'master.')

    def setup():
        """ Set up the master agent by triggering all assigned controllers.
            Each controller will then call the master agent's callback
            methods ``setupAgents()`` and ``setupJobs()``.
        """

    def setupAgents(controller, agentSpecs):
        """ Callback for loading agent specifications from the controller
            and setting up the corresponding agents.

            Will be called upon agent setup and later when the controller
            wants to provide new agent information.
        """

    def setupJobs(controller, jobSpecs):
        """ Callback for loading the specifications of active jobs from
            the controller and scheduling the corresponding jobs.

            Will be called upon agent setup and later when the controller
            wants to provide new job information.
        """

    def inform(job, result=None, message=''):
        """ Callback for informing the master about the state of a job.
            The result is an IResource object (if not None).
        """


class ICrawler(IAgent):
    """ Collects resources.
    """

    def collect(filter=None):
        """ Return a deferred that upon callback will provide a
            collection of resource objects that should be transferred
            to the server.

            Use the selection criteria given to filter the resources that
            should be collected.
        """


class ITransporter(IAgent):
    """ Transfers one or more collected resources and corresponding
        metadata to another entity - a remote agent or another application.
    """

    serverURL = Attribute('URL of the server the resources will be '
                          'transferred to. The URL also determines the '
                          'transfer protocol, e.g. HTTP or FTP.')
    method = Attribute('Transport method, e.g. PUT.')
    machineName = Attribute('Name under which the local machine is '
                            'known to the server.')
    userName = Attribute('User name for logging in to the server.')
    password = Attribute('Password for logging in to the server.')

    def transfer(resource):
        """ Transfer the resource (an object providing IResource)
            to the server and return a Deferred.
        """


# job control

class IController(Interface):
    """ Fetches agent and job specifications from a control
        storage and updates the storage with the status and result
        information.
    """

    def setupAgent():
        """ Set up the controllers's agent by calling the agent's
            callback methods.
        """


class IScheduler(Interface):
    """ Manages jobs and cares that they are started at the appropriate
        time by the agents responsible for it.
    """

    def schedule(job, startTime=None):
        """ Register the job given for execution at the intended start
            date/time (an integer timestamp) and return the job.

            If the start time is not given schedule the job for immediate
            start. Return the start time with which the job has been
            scheduled - this may be different from the start time
            supplied.
        """


# jobs

class IScheduledJob(Interface):
    """ A job that will be executed on some external triggering at
        a predefined date and time - this is the basic job interface.
    """

    identifier = Attribute('A name/ID unique within the realm of the '
                       'controller.')
    scheduler = Attribute('Scheduler that controls this job.')
    agent = Attribute('Agent responsible for executing the job.')
    controller = Attribute('Controller that issued the job.')
    startTime = Attribute('Date/time at which the job should be executed.')
    params = Attribute('Mapping with key/value pairs to be used by '
                       'the ``execute()`` method.')
    state = Attribute('An object representing the current state of the job.')
    repeat = Attribute('Number of seconds after which the job should be '
                       'rescheduled. Do not repeat if 0.')
    successors = Attribute('Jobs to execute immediately after this '
                       'one has been finished.')

    def execute():
        """ Execute the job, typically by calling the ``execute()`` method
            of the agent responsible for it.
        """

    def reschedule(startTime):
        """ Re-schedule the job, setting the date/time the job should be
            executed again.
        """


class ICrawlingJob(IScheduledJob):
    """ A job specifying a crawling task.
    """

    predefinedMetadata = Attribute('A mapping with metadata to be used '
                                   'for all resources found.')


class ITransportJob(IScheduledJob):
    """ A job managing the the transfer of a resource to the server.
    """

    transporter = Attribute('The transporter agent to use for transfer.')


# information objects

class IResource(Interface):
    """ Represents a data object that is collected by a crawler and
        will be transferred to the server.
    """

    data = Attribute('A string, file, or similar representation of the '
                    'resource\'s content; may be None if the receiver of '
                    'the information can retrieve the date from the path '
                    'given.')
    path = Attribute('A filesystem path or some other information '
                    'uniquely identifying the resource on the client '
                    'machine for the current user.')
    application = Attribute('The name of the application that provided '
                    'the resource, e.g. "filesystem" or "mail".')
    metadata = Attribute('Information describing this resource; '
                    'should be an IMetadataSet object.')


class IMetadataSet(Interface):
    """ Metadata associated with a resource; a mapping.
    """

    def asXML():
        """ Return an XML string representing the metadata set.

            If this metadata set contains other metadata sets
            (nested metadata) these will be converted to XML as well.
        """

    def set(key, value):
        """ Set a metadata element.

            The value may be a string or another metadata set
            (nested metadata).
        """


# logging

class ILogger(Interface):
    """ Ordered collection (list) of log records, probably stored on some
        external device.
    """

    externalLoggers = Attribute('A collection of logger objects '
                    'to which the logging records should be written.')

    def setup():
        """ Initialize the logger with the current configuration settings.
        """

    def log(data):
        """ Record the information given by the ``data`` argument
            (a mapping).
        """


class ILogRecord(Interface):
    """
    """

    def __str__():
        """ Return a string representation suitable for writing to a
            log file.
        """

