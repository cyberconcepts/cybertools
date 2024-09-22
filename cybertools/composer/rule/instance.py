# cybertools.rule.instance

""" Rule instance and related classes.
"""

from zope import component
from zope.component import adapts
from zope.interface import Interface, implementer

from cybertools.composer.instance import Instance
from cybertools.composer.rule.interfaces import IRuleInstance, IActionHandler


@implementer(IRuleInstance)
class RuleInstance(Instance):

    adapts(Interface)

    template = None
    event = None

    def applyTemplate(self, **kw):
        for c in self.template.conditions:
            cond = component.getAdapter(self, ICondition, name=c)
            if not cond():
                continue
        data = dict(request=self.event.request)
        for action in self.template.actions:
            handler = component.getAdapter(self, IActionHandler,
                                           name=action.handlerName)
            data = handler(data, action.parameters)
        return data

