================================================
Agents for Job Execution and Communication Tasks
================================================

  ($Id$)


Communication Handling
======================

Communication services are provided by handlers specified in the ``talk``
package.

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
