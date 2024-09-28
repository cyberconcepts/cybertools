# loops.composer.layout.browser.liquid.default

""" Default layouts for the liquid skin.
"""

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope import component

from cybertools.browser.liquid import Liquid
from cybertools.browser.renderer import RendererFactory
from cybertools.composer.layout.base import Layout
from cybertools.composer.layout.browser.standard import standardRenderers

defaultRenderers = RendererFactory(ViewPageTemplateFile('default.pt'))


Layout('css.liquid', 'page.css', renderer=standardRenderers['css'],
       media='all', resource='liquid.css', skin=Liquid)

Layout('body.liquid', 'page.body', renderer=defaultRenderers.body,
       skin=Liquid)

