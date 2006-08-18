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
A generic view class.

$Id$
"""

from zope import component
from zope.interface import Interface, implements
from zope.cachedescriptors.property import Lazy
from zope.publisher.interfaces.browser import ISkin
from zope.app.pagetemplate import ViewPageTemplateFile


mainTemplate = ViewPageTemplateFile('main.pt')


class UnboundTemplateFile(ViewPageTemplateFile):

    def __get__(self, instance, type):
        return self


class BodyTemplateView(object):
    """ Dummy view used for providing a body template.
    """

    bodyTemplate = UnboundTemplateFile('liquid/body.pt')


class GenericView(object):

    index = mainTemplate

    template = macro = menu = skin = None

    def setController(self, controller):
        # make the (one and only controller) available via the request
        viewAnnotations = self.request.annotations.setdefault('cybertools.browser', {})
        viewAnnotations['controller'] = controller
        if getattr(controller, 'skinName', None):
            self.setSkin(controller.skinName.value)
        controller.skin = self.skin
        # this is the place to register special macros with the controller:
        self.setupController()
    def getController(self):
        viewAnnotations = self.request.annotations.setdefault('cybertools.browser', {})
        return viewAnnotations.get('controller', None)
    controller = property(getController, setController)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, *args, **kw):
        return self.index(*args, **kw)

    def setupController(self):
        pass

    @Lazy
    def item(self):
        return self

    def pageBody(self):
        bodyTemplate = component.getMultiAdapter((self.context, self.request),
                                                 name='body.html').bodyTemplate
        return bodyTemplate(self)

    def setSkin(self, skinName):
        skin = None
        if skinName:
            skin = component.queryUtility(ISkin, skinName)
            if skin:
                applySkin(self.request, skin)
        self.skin = skin


