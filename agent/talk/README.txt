================================================
Agents for Job Execution and Communication Tasks
================================================

  ($Id$)


Communication Handling
======================

Communication services are provided by handlers specified in the ``talk``
package.

Set up and start an agent with a server
---------------------------------------

  >>> config = '''
  ... controller(names=['core.sample'])
  ... scheduler(name='core')
  ... logger(name='default', standard=30)
  ... talk.server(names=['http'])
  ... talk.server.http(port=8081)
  ... talk.http(handler='testing')
  ... '''
  >>> from cybertools.agent.main import setup
  >>> master = setup(config)
  Starting agent application...
  Using controllers core.sample.
  Setting up HTTP handler for port 8081.

  >>> master.servers
  [<cybertools.agent.talk.http.HttpServer object...>]

We also provide a class to be used for creating subscribers, i.e. objects
that receive messages.

  >>> class Subscriber(object):
  ...     def __init__(self, name):
  ...         self.name = name
  ...     def onMessage(self, interaction, data):
  ...         print ('%s receiving: interaction=%s, data=%s' %
  ...                       (self.name, interaction, data))

  >>> serverSub = Subscriber('server')

  >>> master.servers[0].subscribe(serverSub, 'testing')

Set up a client
---------------

In order to simplify the testing we do not set up a separate agent to
work with the client but handle the client directly.

  >>> from cybertools.agent.talk.http import HttpClient
  >>> client = HttpClient(master)

  >>> clientSub = Subscriber('client')

  >>> session = client.connect(clientSub, 'http://localhost:8081/')

Run the communication dialog
----------------------------

  >>> from cybertools.agent.tests import tester
  >>> tester.iterate(400)
  Session receiving, data={"message": "OK"}


Fin de Partie
=============

  >>> tester.stopThreads()
