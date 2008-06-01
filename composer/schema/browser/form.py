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
View(s) for forms based on composer.schema.

$Id$
"""

from zope import component, interface
from zope.app.container.interfaces import INameChooser
from zope.cachedescriptors.property import Lazy
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.traversing.browser.absoluteurl import absoluteURL

from cybertools.browser.interfaces import IRenderers
from cybertools.composer.interfaces import IInstance
from cybertools.composer.schema.browser.common import schema_macros, schema_edit_macros
from cybertools.composer.schema.interfaces import ISchemaFactory
from cybertools.composer.schema.schema import FormState


class Form(object):

    interface = Interface
    fieldHandlers = {}          # default, don't update!
    formState = FormState()     # dummy, don't update!
    message = u'Object changed.'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def fieldRenderers(self):
        """ proof-of-concept - get a dictionary of renderers (macros) via
            adaptation.
        """
        return IRenderers(self)

    @Lazy
    def fieldEditRenderers(self):
        return schema_edit_macros.macros

    @Lazy
    def object(self):
        return self.context

    @Lazy
    def schema(self):
        schemaFactory = component.getAdapter(self.object, ISchemaFactory)
        return schemaFactory(self.interface, manager=self,
                             request=self.request)

    @Lazy
    def fields(self):
        return [f for f in self.schema.fields if not f.readonly]

    @Lazy
    def data(self):
        """ Provide data based on context object.
            May be overwritten by subclass.
        """
        instance = self.instance
        instance.template = self.schema
        data = instance.applyTemplate(mode='edit')
        form = self.request.form
        for k, v in data.items():
            #overwrite data with values from request.form
            if k in form:
                data[k] = form[k]
        return data

    @Lazy
    def instance(self):
        return IInstance(self.object)

    def update(self):
        """ Process form data - store in context object.
            May be overwritten by subclass.
        """
        form = self.request.form
        if not form.get('action'):
            return True
        obj = self.object
        instance = component.getAdapter(obj, IInstance, name='editor')
        instance.template = self.schema
        self.formState = formState = instance.applyTemplate(data=form,
                                       fieldHandlers=self.fieldHandlers)
        if formState.severity > 0:
            # show form again
            return True
        if formState.changed:
            notify(ObjectModifiedEvent(obj))
        url = '%s?messsage=%s' % (self.nextUrl, self.message)
        self.request.response.redirect(url)
        return False

    @Lazy
    def nextUrl(self):
        return absoluteURL(self.object, self.request)


class CreateForm(Form):

    factory = None      # overwrite!
    message = u'Object created.'

    @Lazy
    def object(self):
        return self.factory()

    @Lazy
    def container(self):
        return self.context

    def update(self):
        form = self.request.form
        if not form.get('action'):
            return True
        obj = self.object
        instance = component.getAdapter(obj, IInstance, name='editor')
        instance.template = self.schema
        self.formState = formState = instance.applyTemplate(data=form,
                                       fieldHandlers=self.fieldHandlers)
        if formState.severity > 0:
            # show form again
            return True
        container = self.container
        name = self.getName(obj)
        container[name] = obj
        notify(ObjectCreatedEvent(obj))
        notify(ObjectModifiedEvent(obj))
        url = '%s?messsage=%s' % (self.nextUrl, self.message)
        self.request.response.redirect(url)
        return False

    def getName(self, obj):
        name = getattr(obj, 'name', getattr(obj, 'title'))
        return INameChooser(container).chooseName(name, obj)


# proof-of-concept - define a dictionary of renderers (macros) as an adapter
@interface.implementer(IRenderers)
@component.adapter(Form)
def getFormSchemaRenderers(view):
    return schema_macros.macros
component.provideAdapter(getFormSchemaRenderers)

