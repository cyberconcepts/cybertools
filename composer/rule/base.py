#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Basic classes for rules and actions.

$Id$
"""

from zope import component
from zope.component import adapts
from zope.interface import implements

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.interfaces import IInstance
from cybertools.composer.rule.interfaces import IRuleManager, IRule
from cybertools.composer.rule.interfaces import IRuleInstance
from cybertools.composer.rule.interfaces import IEvent, ICondition
from cybertools.composer.rule.interfaces import IAction, IActionHandler
from cybertools.util.jeep import Jeep


# rules

class RuleManager(object):

    implements(IRuleManager)

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
        return self.rules.get(event.name, [])

    def handleEvent(self, event):
        rules = self.getRulesForEvent(event)
        for r in rules:
            ri = IRuleInstance(event.context)
            ri.template = r
            ri.event = event
            ri.applyTemplate()


class Rule(Template):

    implements(IRule)

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


class RuleInstance(object):

    implements(IInstance)

    template = None

    def applyTemplate(self):
        pass


# events

class EventType(object):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name


class Event(object):

    implements(IEvent)

    def __init__(self, eventType, context=None):
        self.eventType = eventType
        self.name = eventType.name
        self.title = eventType.title
        self.context = context


# conditions

class Condition(object):

    implements(ICondition)
    adapts(IRuleInstance)

    def __init__(self, context):
        self.context = context

    def __call__(self, context, params):
        return True


# actions

class Action(Component):

    implements(IAction)

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


class ActionHandler(object):

    implements(IActionHandler)
    adapts(IRuleInstance)

    def __init__(self, context):
        self.context = context

    def __call__(self, data, params={}):
        return data
