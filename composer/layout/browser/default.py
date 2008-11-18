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
Default layouts.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile

from cybertools.browser.renderer import RendererFactory
from cybertools.composer.layout.base import Layout
from cybertools.composer.layout.browser.standard import standardRenderers


defaultRenderers = RendererFactory(ViewPageTemplateFile('default.pt'))


page = Layout('page', 'page', renderer=standardRenderers['page'],
              sublayouts=set(['css.liquid', 'body.liquid']),
              favicon='default/favicon.png')

logo = Layout('logo.default', 'body.logo', renderer=defaultRenderers.logo)

top_actions = Layout('top_actions.default', 'body.top_actions',
                     renderer=defaultRenderers.top_actions)

column1 = Layout('column1.default', 'body.column1',
                 renderer=defaultRenderers.column1)

content = Layout('content.default', 'body.content',
                 renderer=defaultRenderers.content)

column2 = Layout('column2.default', 'body.column2',
                 renderer=defaultRenderers.column2)

footer = Layout('footer.default', 'body.footer', renderer=defaultRenderers.footer)
