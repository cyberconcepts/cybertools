#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Classes for wiki-specific views.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.traversing.browser import absoluteURL

from cybertools.link.interfaces import ILinkManager


class WikiBaseView(object):

    default_template = ViewPageTemplateFile('default.pt')


class WikiManagerView(WikiBaseView):

    content_renderer = 'manager'

    def update(self):
        form = self.request.form
        return True

    def listWikis(self):
        return self.context.listWikis()


class WikiView(WikiBaseView):

    content_renderer = 'wiki'

    def update(self):
        return True

    def listPages(self):
        return self.context.listPages()


class CreatePage(object):

    def update(self):
        form = self.request.form
        name = form.get('name')
        title = name
        page = self.context.createPage(name, title)
        # record in LinkManager
        manager = self.context.getManager()
        lmName = self.context.getConfig('linkManager')
        lm = manager.getPlugin(ILinkManager, lmName)
        for link in lm.query(name=name):
            if link.target is None:
                link.update(target=page)
        self.request.response.redirect('%s?mode=edit' %
                absoluteURL(page, self.request))
        return False


class WikiPageView(WikiBaseView):

    content_renderer = 'wikipage'

    def update(self):
        form = self.request.form
        if form.get('form_action') == 'edit':
            title = form.get('title')
            if title and title != self.context.title:
                self.context.title = title
            text = form.get('text')
            if text and text != self.context.text:
                self.context.text = text
            # TODO: notify(ObjectModifiedEvent())
            #self.request.response.redirect(absoluteURL(self.context, self.request))
            #return False
        return True

    def render(self):
        return self.context.render(self.request)
