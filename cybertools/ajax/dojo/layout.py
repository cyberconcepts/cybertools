#
#  Copyright (c) 2008 Helmut Merz - helmutm@cy55.de
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
Embed Dojo using the cybertools.composer.layout procedure.

$Id$
"""

from cStringIO import StringIO
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

from cybertools.browser.renderer import RendererFactory
from cybertools.composer.layout.base import Layout, LayoutInstance
from cybertools.composer.layout.browser.standard import standardRenderers

dojoRenderers = RendererFactory(ViewPageTemplateFile('macros.pt'))


dojo = Layout('js.dojo', 'page.js', renderer=dojoRenderers.dojo,
                instanceName='dojo', order=0)

dojoRequire = Layout('js.dojo.require', 'page.js',
                renderer=dojoRenderers.dojo_require,
                instanceName='dojo', order=50)

dojoCss = Layout('css.dojo', 'page.css', renderer=standardRenderers.css,
             media='all', resource='ajax.dojo/dojo/resources/dojo.css',
             order=10)

dojoCssTundra = Layout('css.dojo.tundra', 'page.css', renderer=standardRenderers.css,
             media='all', resource='ajax.dojo/dijit/themes/tundra/tundra.css',
             order=11)

dojoCssLightbox = Layout('css.dojo.lightbox', 'page.css', renderer=standardRenderers.css,
             media='all', resource='ajax.dojo/dojox/image/resources/Lightbox.css',
             order=12)

dojoCssScrollPane = Layout('css.dojo.scrollpane', 'page.css', renderer=standardRenderers.css,
             media='all', resource='ajax.dojo/dojox/layout/resources/ScrollPane.css',
             order=13)


class DojoLayoutInstance(LayoutInstance):

    djConfig = "parseOnLoad: true, usePlainJson: true, locale: 'de'"

    @Lazy
    def content(self):
        djInfo = self.view.request.annotations.get('ajax.dojo', {})
        packages = djInfo.get('requirements', set())
        out = StringIO()
        for p in packages:
            out.write("dojo.require('%s'); " % p)
        return out.getvalue()
