===========================
Meta Information Management
===========================

  ($Id$)


Configuration Options, Settings, Preferences
============================================

  >>> from cybertools.meta.config import Options

  >>> config = Options()

The Options object allows us to access arbitrary attributes that will
be created as elements within the Options object.

  >>> config.storage
  <AutoElement 'storage'>

  >>> config.i18n.languages = ['de', 'en', 'it']

  >>> config.i18n.languages
  ['de', 'en', 'it']

  >>> config('i18n.languages')
  ['de', 'en', 'it']

Loading options as Python code
------------------------------

  >>> from cybertools.meta.namespace import Executor
  >>> config = Options()
  >>> ex = Executor(config)

  >>> code = """
  ... controller(names=('cmdline', 'telnet'))
  ... controller.telnet(port= 5001)
  ... scheduler(name='core')
  ... logger(name='default', standard=30)
  ... """

  >>> result = ex.execute(code)

  >>> config.scheduler.name
  'core'
  >>> config.logger.standard
  30
  >>> config.controller.names
  ('cmdline', 'telnet')
  >>> config.controller.telnet.port
  5001

  >>> print config
  controller.telnet(port=5001)
  controller(names=('cmdline', 'telnet'))
  scheduler(name='core')
  logger(name='default', standard=30)

