#
#  Copyright (c) 2011 Helmut Merz helmutm@cy55.de
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
Controller for views, templates, macros.

$Id$
"""

from zope import component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

from cybertools.browser.configurator import IViewConfigurator, IMacroViewProperty
from cybertools.browser.member import IMemberInfoProvider
from cybertools.util.jeep import Jeep


# layout controller: collects information about head elements, skins, portlets, etc

class Controller(object):

    def __init__(self, context, request):
        self.view = view = context         # the controller is adapted to a view
        self.context = context.context
        self.request = request
        self.params = Jeep()
        self.templates = {}
        self.configure()
        #self.view.setupController()
        self.view.controller = self   # notify the view

    skin = None         # may be overwritten by the view

    @Lazy
    def macros(self):
        return Macros(self)

    @Lazy
    def resourceBase(self):
        skinSetter = self.skin and ('/++skin++' + self.skin.__name__) or ''
        # TODO: put '/@@' etc after path to site instead of directly after URL0
        return self.request.URL[0] + skinSetter + '/@@/'

    def configure(self):
        # collect multiple configurators:
        configurators = component.getAdapters((self.context, self.request),
                                              IViewConfigurator)
        for conf in configurators:
            configurator = conf[1]
            for item in configurator.getActiveViewProperties():
                if IMacroViewProperty.providedBy(item):
                    self.macros.register(item.slot, item.identifier,
                                         item.template, item.name,
                                         **item.params)
                else:
                    setattr(self, item.slot, item)

    @Lazy
    def memberInfo(self):
        provider = component.queryMultiAdapter((self.context, self.request),
                                          IMemberInfoProvider)
        return provider is not None and provider.data or None

    def setMainPage(self):
        # May be overridden by subclasse for setting special main index template
        pass

    def getTemplateMacros(self, name, default):
        template = self.templates.get(name)
        if template is None:
            template = default
        return template.macros

    def mergeTemplateMacros(self, name, *bases):
        result = {}
        for base in bases:
            result.update(base.macros)
        template = self.templates.get(name)
        if template is not None:
            result.update(template.macros)
        return result


class Macros(dict):

    standardTemplate = ViewPageTemplateFile('base_macros.pt')

    def __init__(self, controller):
        self.controller = controller
        self.identifiers = {}

    def register(self, slot, identifier=None, template=None, name=None,
                 priority=50, **kw):
        if identifier:
            # make sure a certain resource is only registered once
            if identifier in self.identifiers:
                return
        if template is None:
            template = self.standardTemplate
        if name is None:
            name = slot
        macro = Macro(template, name, priority, identifier=identifier, **kw)
        entry = self.setdefault(slot, [])
        entry.append(macro)
        if identifier:
            self.identifiers[identifier] = macro

    def hide(self, identifier):
        self.identifiers[identifier] = False

    def __getitem__(self, key):
        return [m for m in sorted(self.get(key, []), key=lambda x: x.priority)
                  if self.identifiers.get(m.identifier, True)]


class Macro(object):

    identifier = ''

    def __init__(self, template, name, priority, **kw):
        self.template = template
        self.name = name
        self.priority = priority
        for k in kw:
            setattr(self, k, kw[k])

    @Lazy
    def macro(self):
        return self.template.macros[self.name]

    def __call__(self):
        return self.macro

