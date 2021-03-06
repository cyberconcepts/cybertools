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
Rule instance and related classes.

$Id$
"""

from zope import component
from zope.component import adapts
from zope.interface import Interface, implements

from cybertools.composer.instance import Instance
from cybertools.composer.rule.interfaces import IRuleInstance, IActionHandler


class RuleInstance(Instance):

    implements(IRuleInstance)
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

