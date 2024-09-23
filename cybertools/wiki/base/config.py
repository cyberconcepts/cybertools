# cybertools.wiki.base.config

""" Basic Configuration implementations.
"""

from zope.interface import implementer

from cybertools.wiki.interfaces import IWikiConfigInfo, IWikiConfiguration


@implementer(IWikiConfigInfo)
class WikiConfigInfo(dict):

    def set(self, functionality, value):
        self[functionality] = value

    def __getattr__(self, attr):
        return self.get(attr, None)


class BaseConfigurator(object):

    def __init__(self, context):
        self.context = context

    def initialize(self):
        ci = WikiConfigInfo()
        self.context._configInfo = ci
        return ci

    def getConfigInfo(self):
        return self.context._configInfo


@implementer(IWikiConfiguration)
class BaseConfiguration(object):
    """ The base class for all wiki configuration implementations.
    """

    configurator = BaseConfigurator

    _configInfo = None

    def getConfigInfo(self):
        return self.configurator(self).getConfigInfo()

    def getConfig(self, functionality):
        c = None
        ci = self.getConfigInfo()
        if ci is not None:
            c = ci.get(functionality)
        if c is None:
            parent = self.getConfigParent()
            if parent is not None:
                return parent.getConfig(functionality)
        return c

    def setConfig(self, functionality, value):
        ci = self.getConfigInfo()
        if ci is None:
            ci = self.configurator(self).initialize()
        ci.set(functionality, value)

    def getConfigParent(self):
        return None


class WikiConfiguration(BaseConfiguration):
    """ A global utility providing the default settings.
    """

    _configInfo = WikiConfigInfo(
                    parser='docutils.rstx',
                    writer='docutils.html',
                    linkManager='basic',
                    nodeProcessors=dict(reference=['default'],
                                        image=['default']),
                    mediaManager='default',
    )
