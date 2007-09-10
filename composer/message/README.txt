==================
Message Management
==================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.message.base import MessageManager, Message

  >>> manager = MessageManager()

  >>> manager.messages.append(Message('feedback_html', manager=manager))
  >>> manager.messages.append(Message('feedback_text', manager=manager))
  >>> manager.messages.append(Message('footer', manager=manager))

  >>> messageText = '''Dear $person.firstname $person.lastname,
  ... You have been registered for the following $services.
  ... $@@list_registrations
  ... $footer
  ... '''

  >>> manager.messages['feedback_text'].text = messageText
  >>> manager.messages['footer'].text = 'Best regards, $sender'

  >>> manager.messages.append(Message('sender', manager=manager, text='Jack'))
  >>> manager.messages.append(Message('services', manager=manager, text='events'))

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
  >>> print mi.applyTemplate()
  Dear $person.firstname $person.lastname,
  You have been registered for the following events.
  $@@list_registrations
  Best regards, Jack
  <BLANKLINE>
