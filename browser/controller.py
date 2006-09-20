#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
from zope.interface import Interface, implements
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

from cybertools.browser.configurator import IViewConfigurator, IMacroViewProperty


# layout controller: collects information about head elements, skins, portlets, etc

class Controller(object):

    def __init__(self, context, request):
        self.view = view = context         # the controller is adapted to a view
        self.context = context.context
        self.request = request
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
        #configurator = component.queryMultiAdapter((self.context, self.request),
        #                                           IViewConfigurator)
        # idea: collect multiple configurators:
        configurators = component.getAdapters((self.context, self.request),
                                              IViewConfigurator)
        for conf in configurators:
            configurator = conf[1]
        #if configurator is not None:
            #for item in configurator.viewProperties:
            for item in configurator.getActiveViewProperties():
                if IMacroViewProperty.providedBy(item):
                    self.macros.register(item.slot, item.idenitifier,
                                         item.template, item.name,
                                         **item.params)
                else:
                    setattr(self, item.slot, item)


class Macros(dict):

    standardTemplate = ViewPageTemplateFile('base_macros.pt')

    def __init__(self, controller):
        self.controller = controller
        self.identifiers = set()

    def register(self, slot, identifier=None, template=None, name=None,
                 position=None, **kw):
        if identifier:
            # make sure a certain resource is only registered once
            if identifier in self.identifiers:
                return
            self.identifiers.add(identifier)
        if template is None:
            template = self.standardTemplate
        if name is None:
            name = slot
        macro = Macro(template, name, **kw)
        entry = self.setdefault(slot, [])
        if position is None:
            entry.append(macro)
        else:
            entry.insert(position, macro)

    def __getitem__(self, key):
        return self.get(key, [])


class Macro(object):

    def __init__(self, template, name, **kw):
        self.template = template
        self.name = name
        for k in kw:
            setattr(self, k, kw[k])

    @Lazy
    def macro(self):
        return self.template.macros[self.name]

    def __call__(self):
        return self.macro


# form processing:
# the part of the model/view/controller pattern that deals with
# form input

class IFormController(Interface):
    """ Used as a named adapter by GenericView for processing form input.
    """

    def update():
        """ Processing form input...
        """


class FormController(object):

    implements(IFormController)

    def __init__(self, context, request):
        self.view = view = context         # the controller is adapted to a view
        self.context = context.context
        self.request = request

    def update(self):
        pass

