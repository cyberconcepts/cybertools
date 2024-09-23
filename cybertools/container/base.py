# cybertools.container.base

""" Ordered container implementation.
"""

from zope.app.container.browser.contents import JustContents
from zope.browserpage import ViewPageTemplateFile
from zope.i18nmessageid import ZopeMessageFactory as _
from zope.cachedescriptors.property import Lazy
from zope.interface import Interface


contents_template = ViewPageTemplateFile('contents.pt')


class ContainerView(JustContents):

    def checkMoveAction(self):
        pass

    orderable = False

    # informations for the ajax.inner.html view (template):

    template = contents_template

    #@Lazy
    #def template(self):
    #    basicView = zapi.getMultiAdapter((self.context, self.request),
    #                    Interface, name=u'contents.html')
    #    return basicView.index

    @Lazy
    def macro(self):
        return self.template.macros['contents']

