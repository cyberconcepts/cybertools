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
cybertools interface definitions.

$Id$
"""

from zope.interface import Interface
from zope.app.container.interfaces import IOrderedContainer
from zope.app.component.interfaces.registration import IRegisterable

from zope.schema import Text, TextLine, List, Object, Int


class IBaseMenuItem(IOrderedContainer):
    """ Base interface with common methods for IMenu and IMenuItem.
    """

    title = TextLine(
        title=u'Title',
        description=u'Title of the menu or text that will appear on the menu item',
        default=u'',
        required=True)

    def getMenuItems():
        """ Return sub-menu items contained in this menu or menu item.
        """

    def addMenuItem(id, title, description='', target=None, urlPath=''):
        """ Add a new menu item to this item or menu. Return the newly
            created menu item.

            This is a convenience method for creating menu structures
            programmatically.
        """

    def getParentMenuItem(menu=None, accu=[]):
        """ Return the menu or menu item this item is a sub menu item.

            For certain cases of dynamic menu generation it may be
            useful to give this method the menu object to which the
            parent menu item path may eventually lead, and a list
            of already accumulated menu items - in order to avoid
            infinite cyclic searches for parent menu items.
        """

    def getMenu():
        """ Return the top-most menu object.
        """


class IMenu(IBaseMenuItem, IRegisterable):
    """ A Menu is a container for MenuItems and will be shown in a
        menu portlet.
    """

    def getActiveMenuItems(context):
        """ Return a a tuple with two elements:
            [0] list with basic (current) menu item objects that
                are associtated with the context.
            [1] list with all menu item objects that lead to
                the context object.
        """

    def getCorrespondingMenuItems(context):
        """ Return the menu items of which context is the target.
        """

    def menuItemPath():
        """ Used for index creation: returns normalized urlPath attribute
            for efficiently finding correspondign menu items via the
            context object's path.
        """


class IMenuItem(IBaseMenuItem):
    """ A MenuItem is part of a Menu and usually displayed together
        with other MenuItem objects in a menu portlet.
    """

    target = Object(Interface,
        title=u'Target',
        description=u'Target object this menu item should link to.',)

    urlPath = TextLine(
        title=u'URL or Path',
        description=u'URL or path that this menu item should link to.',
        default=u'',
        required=True)

    def getItemUrl():
        """ Return the target URL of this menu item.
        """

    def getTargetUrl():
        """ Return the target URL of this menu item.
        """

    def getTargetObject():
        """ Return the object this menu item points to.
        """

    def isActive(context):
        """ Return True if this menu item leads to the context object.
        """

    def isCurrent(context):
        """ Return True if this menu item is associated with the
            context object.
        """

    def menuItemPath():
        """ Used for index creation: returns normalized urlPath attribute
            for efficiently finding correspondign menu items via the
            context object's path.
        """

