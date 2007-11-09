==================
Message Management
==================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.message.base import MessageManager, Message

  >>> manager = MessageManager()

  >>> messageText = '''Dear $person.firstname $person.lastname,
  ... You have been registered for the following $services.
  ... $@@list_registrations
  ... $footer
  ... '''

  >>> manager.addMessage('feedback_text', messageText)
  >>> manager.addMessage('footer', 'Best regards, $sender')
  >>> manager.addMessage('sender', 'Jack')
  >>> manager.addMessage('services', 'events')

Message interpolation
---------------------

  >>> from cybertools.composer.message.instance import MessageTemplate
  >>> t = MessageTemplate(messageText)
  >>> print t.safe_substitute({
  ...           'person.firstname': 'John', 'person.lastname': 'Smith',
  ...           '@@list_registrations': '0815: Python Introduction',
  ...           'services': 'events',
  ...           'footer': 'Regards, $sender'})
  Dear John Smith,
  You have been registered for the following events.
  0815: Python Introduction
  Regards, $sender
  <BLANKLINE>

Working with message instances
------------------------------

  >>> from cybertools.composer.message.instance import MessageInstance
  >>> mi = MessageInstance(None, manager.messages['feedback_text'])
  >>> for key, value in mi.applyTemplate().items():
  ...     print key + ':', value
  subject:
  text: Dear $person.firstname $person.lastname,
  You have been registered for the following events.
  $@@list_registrations
  Best regards, Jack
  <BLANKLINE>
