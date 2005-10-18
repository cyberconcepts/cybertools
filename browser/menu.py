#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
cybertools menu.

$Id$
"""

from zope.app import zapi
from zope.app.pagetemplate.simpleviewclass import simple
from zope.viewlet.viewlet import ViewletBase, SimpleViewletClass
from zope.app.publisher.interfaces.browser import IBrowserMenu


class MenuViewlet(ViewletBase):
    """ Menu viewlet.
    """

    def getMenu(self):
        menu = zapi.getUtility(IBrowserMenu, name='mmain')
        return menu
    

def GenericMenuViewlet(template, offering=None, bases=(), name=u'', weight=0):
    #return SimpleViewletClass(template, offering,
    #                bases + (MenuViewletBase,), name, weight)
    if offering is None:
        offering = sys._getframe(1).f_globals
    bases += (MenuViewletBase, simple)
    class_ = type("GenericMenuViewlet from %s" % template, bases,
                  {'index' : ViewletPageTemplateFile(template, offering),
                   '_weight' : weight,
                   '__name__' : name})
    return class_


                    