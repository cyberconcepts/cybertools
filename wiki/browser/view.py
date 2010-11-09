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
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.traversing.browser import absoluteURL

from cybertools.link.interfaces import ILinkManager


class WikiBaseView(object):

    default_template = ViewPageTemplateFile('default.pt')
    template = default_template

    @Lazy
    def actions(self):
        return dict(top=[],
                    portlet_left=[self.default_template.macros['navigation']],
                    portlet_right=[])

    def configForEditing(self):
        lines = []
        for k, v in self.context.getConfigInfo().items():
            if isinstance(v, (list, tuple)):
                v = '[%s]' % ', '.join(v)
            if v is None:
                v = ''
            lines.append('%s: %s' % (k, v))
        return '\n'.join(lines)


class WikiManagerView(WikiBaseView):

    content_renderer = 'manager'

    def update(self):
        form = self.request.form
        if form.get('form.action') == 'apply' and 'config' in form:
            self.processConfigData(form['config'])
        return True

    def processConfigData(self, input):
        for line in input.splitlines():
            if line:
                self.processConfigLine(line)

    def processConfigLine(self, line):
        value = None
        k, v = line.split(':', 1)
        key = k.strip()
        v = v.strip()
        if v:
            if v.startswith('[') and v.endswith(']'):
                value = [s.strip() for s in v[1:-1].split(',')]
            else:
                value = v
        if not value:
            value = None
        if value != self.context.getConfig(key):
            self.context.setConfig(key, value)

    def listWikis(self):
        return self.context.listWikis()


class WikiView(WikiBaseView):

    content_renderer = 'wiki'

    def update(self):
        return True

    def listPages(self):
        return self.context.listPages()


class WikiEditForm(WikiView):

    content_renderer = 'wiki_edit'

    def update(self):
        form = self.request.form
        action = form.get('form_action')
        if action == 'edit':
            title = form.get('title')
            if title and title != self.context.title:
                self.context.title = title
                notify(ObjectModifiedEvent(self.context))
            name = form.get('name')
            if name and name != self.context.name:
                self.context.getManager().renameWiki(self.context, name)
            self.request.response.redirect(
                            absoluteURL(self.context, self.request))
            return False
        return True


class CreatePage(object):

    def update(self):
        form = self.request.form
        name = form.get('name')
        title = name
        page = self.context.createPage(name, title)
        notify(ObjectModifiedEvent(page))
        # record in LinkManager
        manager = self.context.getManager()
        lmName = self.context.getConfig('linkManager')
        lm = manager.getPlugin(ILinkManager, lmName)
        for link in lm.query(name=name):
            if link.target is None:
                link.update(target=page)
        self.request.response.redirect('%s/@@edit.html' %
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
            text = toUnicode(form.get('text'))
            if text and text != self.context.text:
                self.context.text = text
            notify(ObjectModifiedEvent(self.context))
        return True

    def render(self):
        return toUnicode(self.context.render(self.request))

    def edit(self):
        self.view_mode = 'edit'
        return self()

    def showEditButton(self):
        return self.view_mode != 'edit'


def toUnicode(text, encoding='UTF-8'):
    if not isinstance(text, str):
        return text
    try:
        return text.decode(encoding)
    except UnicodeDecodeError:
        return text.decode('ISO8859-15')

