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
Definition of the Menu class.

$Id$
"""

from zope.interface import implements
from zope.app.container.ordered import OrderedContainer
from zope.app import zapi

from interfaces import IMenu

class Menu(OrderedContainer):

    implements(IMenu)

    title = u''

    def getMenuItems(self):
        return ()

    def addMenuItem(self, id, title, description='', target=None, urlPath=''):
        pass

    def getParentMenuItem(self, menu=None, accu=[]):
        return None

    def getMenu(self):
        return None
        
    def getActiveMenuItems(self, context):
        return ()

    def getCorrespondingMenuItems(self,context):
        return ()

    def menuItemPath(self):
        return ''
