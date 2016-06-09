#
#  Copyright (c) 2016 Helmut Merz helmutm@cy55.de
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
"""

from logging import getLogger
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.interface import Interface, implements
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.event import notify
from zope.publisher.http import URLGetter as BaseURLGetter
from zope.publisher.interfaces.browser import IBrowserSkinType

from cybertools.browser.renderer import CachableRenderer
import cybertools.util.date


mainTemplate = ViewPageTemplateFile('main.pt')
popupTemplate = ViewPageTemplateFile('liquid/popup.pt')


class IBodyRenderedEvent(Interface):
    """ Is fired when the page body has been rendered. """


class BodyRenderedEvent(object):

    implements(IBodyRenderedEvent)

    def __init__(self, context, request):
        self.context = context
        self.request = request


class UnboundTemplateFile(ViewPageTemplateFile):

    def __get__(self, instance, type):
        return self


class BodyTemplateView(object):
    """ Dummy view used for providing a body template.
    """

    bodyTemplate = UnboundTemplateFile('liquid/body.pt')


class URLGetter(BaseURLGetter):

    def __str__(self):
        return self.__request.getURL().rstrip('/@@index.html')


class GenericView(object):

    index = mainTemplate

    template = macro = menu = skin = None

    cachableRendererFactory = CachableRenderer

    _updated = False

    def setController(self, controller):
        # make the (one and only controller) available via the request
        viewAnnotations = self.request.annotations.setdefault('cybertools.browser', {})
        viewAnnotations['controller'] = controller
        #if getattr(controller, 'skinName', None) and controller.skinName.value:
        #    self.setSkin(controller.skinName.value)
        controller.skin = self.skin
        # this is the place to register special macros with the controller:
        self.setupController()
    def getController(self):
        viewAnnotations = self.request.annotations.setdefault('cybertools.browser', {})
        cont = viewAnnotations.get('controller', None)
        if cont is None:
            cont = component.queryMultiAdapter((self, self.request), name='controller')
            #if cont is not None:
            #    self.setController(cont)
        return cont
    controller = property(getController, setController)

    def __init__(self, context, request):
        self.context = self.__parent__ = context
        self.request = request
        #cont = self.controller  # check: leads to strange AttributeError in doctest
        #if cont is not None:
        #    self.setupController()

    def __call__(self, *args, **kw):
        # this is useful for a top-level page only
        return self.index(*args, **kw)

    @property
    def requestUrl(self):
        return URLGetter(self.request)

    @Lazy
    def isAuthenticated(self):
        return not IUnauthenticatedPrincipal.providedBy(self.request.principal)

    def setupSubviews(self):
        pass

    #def render(self, *args, **kw):
    #    return self.index(*args, **kw)

    def update(self):
        result = True
        if not self._updated:
            action = self.request.form.get('form.action')
            if action:
                fc = component.getMultiAdapter((self, self.request),
                                               name=action)
                result = fc.update()
        self._updated = True
        return result

    def setupController(self):
        """ May be called by __init__() if there is already a controller
            or when the controller is set. May be implemented by subclass.
        """
        pass

    @Lazy
    def item(self):
        return self

    def pageBody(self):
        bodyTemplate = component.getMultiAdapter((self.context, self.request),
                                                 name='body.html').bodyTemplate
        body = bodyTemplate(self)
        notify(BodyRenderedEvent(self.context, self.request))
        return body

    def setSkin(self, skinName):
        skin = None
        if skinName:
            skin = component.queryUtility(IBrowserSkinType, skinName)
            if skin:
                applySkin(self.request, skin)
        self.skin = skin

    def cachedRenderer(self, baseRenderer, *args):
        cr = self.cachableRendererFactory(self, baseRenderer)
        return cr.renderMacro(*args)

    def currentYear(self):
        return cybertools.util.date.year()

    def logInfo(self, message, logName='cybertools'):
        logger = getLogger(logName)
        logger.info(message)

