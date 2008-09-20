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
Default layouts for the liquid skin.

$Id$
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope import component
from zope.interface import implements

from cybertools.browser.liquid import Liquid
from cybertools.composer.layout.base import Layout
from cybertools.composer.layout.browser.standard import standardRenderers

defaultRenderers = ViewPageTemplateFile('default.pt').macros


css = Layout('css.liquid', 'page.css', renderer=standardRenderers['css'],
             media='all', resource='liquid.css', skin=Liquid)

body = Layout('body.liquid', 'page.body', renderer=defaultRenderers['body'],
              skin=Liquid)

