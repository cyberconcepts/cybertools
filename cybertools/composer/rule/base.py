# cybertools.composer.rule.base

""" Basic classes for rules and actions.
"""

from zope import component
from zope.component import adapts
from zope.interface import implementer

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.interfaces import IInstance
from cybertools.composer.rule.interfaces import IRuleManager, IRule
from cybertools.composer.rule.interfaces import IRuleInstance
from cybertools.composer.rule.interfaces import IEvent, ICondition
from cybertools.composer.rule.interfaces import IAction, IActionHandler
from cybertools.util.jeep import Jeep


# rules

@implementer(IRuleManager)
class RuleManager(object):

    rulesFactory = Jeep
    rules = None

    def addRule(self, rule):
        rule.manager = self
        if self.rules is None:
            self.rules = self.rulesFactory()
        for e in rule.events:
            entry = self.rules.setdefault(e.name, [])
            entry.append(rule)

    def getRulesForEvent(self, event):
        return self.rules and self.rules.get(event.name, []) or []

    def handleEvent(self, event):
        result = []
        rules = self.getRulesForEvent(event)
        for r in rules:
            ri = IRuleInstance(event.context)
            ri.template = r
            ri.event = event
            result.append(ri.applyTemplate())
        return result


@implementer(IRule)
class Rule(Template):

    name = title = description = u''
    manager = None
    actions = None
    events = None
    conditions = None

    def __init__(self, name, **kw):
        self.name = name
        for k, v in kw.items():
            setattr(self, k, v)
        self.events = []
        self.conditions = []
        self.actions = []


# events

class EventType(object):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name


@implementer(IEvent)
class Event(object):

    def __init__(self, eventType, context=None, request=None):
        self.eventType = eventType
        self.name = eventType.name
        self.title = eventType.title
        self.context = context
        self.request = request


# conditions

@implementer(ICondition)
class Condition(object):

    adapts(IRuleInstance)

    def __init__(self, context):
        self.context = context

    def __call__(self, context, params):
        return True


# actions

@implementer(IAction)
class Action(Component):

    name = u''
    handlerName = u''
    parameters = None
    rule = None

    def __init__(self, name, **kw):
        self.name = name
        for k, v in kw.items():
            setattr(self, k, v)
        if self.parameters is None:
            self.parameters = {}
        if not self.handlerName:
            self.handlerName = name


@implementer(IActionHandler)
class ActionHandler(object):

    adapts(IRuleInstance)

    def __init__(self, context):
        self.context = context

    def __call__(self, data, params={}):
        return data
