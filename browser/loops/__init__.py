"""
$Id$
"""

from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.rotterdam import Rotterdam
from cybertools.browser.liquid import Liquid


#class Loops(Liquid):
class Loops(Rotterdam):
    """ The Loops skin """
