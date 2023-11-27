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
Ordered container implementation.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.container.browser.contents import JustContents
from zope.app.i18n import ZopeMessageFactory as _
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

