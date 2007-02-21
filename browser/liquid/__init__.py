"""
$Id$
"""

from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.rotterdam import Rotterdam


class liquid(IBrowserRequest):
    """The `liquid` layer."""


class Liquid(liquid, Rotterdam):
    """ The Liquid skin """

