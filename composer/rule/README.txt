===============================
Rule-based Execution of Actions
===============================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.rule.base import RuleManager, Rule, Action
  >>> from cybertools.composer.rule.base import EventType, Event

  >>> from cybertools.composer.rule.instance import RuleInstance
  >>> from cybertools.composer.rule.interfaces import IRuleInstance
  >>> component.provideAdapter(RuleInstance, provides=IRuleInstance)
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

  >>> from cybertools.composer.schema.client import Client
  >>> client = Client()

  >>> manager.handleEvent(Event(checkoutEvent, client))

