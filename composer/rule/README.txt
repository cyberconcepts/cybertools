===============================
Rule-based Execution of Actions
===============================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.rule.base import RuleManager, Rule, Action
  >>> from cybertools.composer.rule.base import EventType, Event

  >>> from cybertools.composer.rule.base import ActionHandler
  >>> component.provideAdapter(ActionHandler, name='message')
  >>> component.provideAdapter(ActionHandler, name='sendmail')

  >>> manager = RuleManager()

  >>> loginEvent = EventType('login')
  >>> checkoutEvent = EventType('service.checkout')

  >>> checkoutRule = Rule('regcheckoutmail', manager=manager)
  >>> checkoutRule.events.append(checkoutEvent)
  >>> checkoutRule.actions.append(Action('message',
  ...                   parameters = dict(messageName='confirmation_mail')))
  >>> checkoutRule.actions.append(Action('sendmail'))
  >>> manager.addRule(checkoutRule)

  >>> manager.handleEvent(Event(loginEvent))

  >>> client = object()

  >>> manager.handleEvent(Event(checkoutEvent, client))

