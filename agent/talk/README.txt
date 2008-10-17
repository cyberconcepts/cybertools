================================================
Agents for Job Execution and Communication Tasks
================================================

  ($Id$)

  >>> config = '''
  ... controller(names=['core.sample'])
  ... scheduler(name='core')
  ... logger(name='default', standard=30)
  ... talk.http = 'testing'
  ... '''
  >>> from cybertools.agent.main import setup
  >>> master = setup(config)
  Starting agent application...
  Using controllers core.sample.


Communication Handling
======================

  >>> from cybertools.agent.talk.http import Handler

