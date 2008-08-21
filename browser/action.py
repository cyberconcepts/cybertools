#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
Base classes (sort of views) for action portlet items.

$Id$
"""

from copy import copy
from urllib import urlencode
from zope import component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

action_macros = ViewPageTemplateFile('action_macros.pt')


class Action(object):

    template = action_macros
    macroName = 'action'
    target = None   # an explicitly specified object, use instead of view.context
    priority = 50
    condition = True
    permission = None
    url = '.'
    viewName = ''
    targetWindow = ''
    title = ''
    description = ''
    icon = ''
    cssClass = ''
    onClick = ''
    innerHtmlId = ''
    prerequisites = []

    def __init__(self, view, **kw):
        self.view = view
        for k, v in kw.items():
            setattr(self, k, v)

    @Lazy
    def macro(self):
        return self.template.macros[self.macroName]

    @Lazy
    def url(self):
        return self.getActionUrl(self.view.url)

    def getActionUrl(self, baseUrl):
        if self.viewName:
            return '/'.join((baseUrl, self.viewName))
        else:
            return baseUrl


class ActionRegistry(object):
    """ Use this object (probably as a global utility) to collect all kinds
        of action definitions that should be available on the system.
    """

    def __init__(self):
        self.actionsByName = {}
        self.actionsByCategory = {}

    def register(self, name, category='object', cls=Action, **kw):
        action = cls(None, name=name, category=category, **kw)
        nameItem = self.actionsByName.setdefault(name, [])
        nameItem.append(action)
        catItem = self.actionsByCategory.setdefault(category, [])
        catItem.append(action)

    def get(self, category=None, names=[], view=None, **kw):
        if view is None:
            raise ValueError("The 'view' argument is missing.")
        if names:
            result = []
            for n in names:
                result.extend(self.actionsByName.get(n, []))
            if category is not None:
                result = [r for r in result if r.category == category]
        elif category is not None:
            result = self.actionsByCategory.get(category, [])
        else:
            raise ValueError("One of 'name' or 'category' arguments must be given.")
        for action in sorted(result, key=lambda x: x.priority):
            action = copy(action)
            action.view = view
            for k, v in kw.items():
                setattr(action, k, v)
            for p in action.prerequisites:
                method = p
                if isinstance(method, str):
                    method = getattr(view, p, None)
                if method is not None:
                    method()
            condition = action.condition
            if not isinstance(condition, bool):
                if isinstance(condition, str):
                    condition = getattr(view, condition, None)
                if callable(condition):
                    condition = condition()
            if not condition:
                continue
            yield action


# TODO: register as a global utility
actions = ActionRegistry()

