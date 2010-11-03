#
#  Copyright (c) 2009 Helmut Merz helmutm@cy55.de
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
Basic Configuration implementations.

$Id$
"""

from zope.interface import implements

from cybertools.wiki.interfaces import IWikiConfigInfo, IWikiConfiguration


class WikiConfigInfo(dict):

    implements(IWikiConfigInfo)

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


class BaseConfiguration(object):
    """ The base class for all wiki configuration implementations.
    """

    implements(IWikiConfiguration)

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
                    nodeProcessors=dict(reference=['default']),
                    mediaManager='default',
    )
