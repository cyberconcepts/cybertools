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
Generic base classes for web-based views.

$Id$
"""

from zope.cachedescriptors.property import Lazy
from cybertools.view import pac
from cybertools.view.web.zpt.template import Template


class View(pac.View):
    """ A generic web-based view - not necessarily HTML-/browser-based.
    """


class BrowserView(View):
    """ A browser-based view (i.e. a view using HTML as presentation language).
    """

    templateFactory = None

    @Lazy
    def template(self):
        return self.templateFactory(self)

    def render(self, *args, **kw):
        return self.template.render(*args, **kw)


class Page(BrowserView):
    """ A browser-based view that renders a full web page.
    """

    templateFactory = Template

    def setUp(self):
        super(Page, self).setUp()
        self.add(Content)


class Content(BrowserView):
    """ A browser-based view that renders the content region of a web page.
    """

