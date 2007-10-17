===============================
Rule-based Execution of Actions
===============================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.rule.base import RuleManager, Rule, Action
  >>> from cybertools.composer.rule.base import EventType, Event

  >>> manager = RuleManager()

  >>> loginEvent = EventType('login')
  >>> checkoutEvent = EventType('service.checkout')

  >>> checkoutRule = Rule('regcheckoutmail', manager=manager)
  >>> checkoutRule.events.append(checkoutEvent)
  >>> checkoutRule.actions.append(Action('message',
  ...                   parameters = dict(messageName='confirmation_mail')))
  >>> checkoutRule.actions.append(Action('sendmail'))
  >>> manager.rules.append(checkoutRule)

  >>> manager.handleEvent(Event(loginEvent))

  >>> client = object()

  >>> manager.handleEvent(Event(checkoutEvent, client))

