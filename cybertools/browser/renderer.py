# cybertools.browser.renderer

""" Use ZPT macros as layout renderers.
"""

from zope.browserpage import ViewPageTemplateFile

from cybertools.util.cache import cache


class RendererFactory(object):
    """ Provider for ZPT macros.
    """

    def __init__(self, template):
        self.template = template

    def get(self, key, default=None):
        return self.template.macros.get(key, default)

    def __getitem__(self, key):
        #return self.template.macros[key]
        return Renderer(key, self)

    def __getattr__(self, key):
        """ Convenience method.
        """
        #return lambda key=key: self[key]
        return self[key]

    def __repr__(self):
        return ('<RendererFactory, template=%r, macros=%r>' %
                    (self.template, self.template.macros.keys()))


class Renderer(object):

    def __init__(self, name, factory):
        self.name = name
        self.factory = factory
        self.template = factory.template

    def __call__(self):
        return self.template.macros[self.name]


rendererTemplate = ViewPageTemplateFile('renderer.pt')

class CachableRenderer(object):

    lifetime = 3 * 3600
    #lifetime = 24 * 3600

    def __init__(self, view, renderer):
        self.view = view
        self.renderer = renderer

    def getRenderMacroId(self, *args):
        return 'renderer.' + '.'.join(args)

    @cache(getRenderMacroId, lifetime=lifetime)
    def renderMacro(self, *args):
        return rendererTemplate(self.view, view=self.view, macro=self.renderer)


