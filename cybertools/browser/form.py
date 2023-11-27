#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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

"""Form Controller stuff: form processing is the part of the
model/view/controller pattern that deals withform input.

$Id$
"""

from zope.interface import Interface, implements


class IFormController(Interface):
    """ Used as a named adapter by GenericView for processing form input.
    """

    def update():
        """ Processing form input...
        """


class FormController(object):

    implements(IFormController)

    def __init__(self, context, request):
        self.view = self.__parent__ = view = context
        self.context = view.context # the controller is adapted to a view
        self.request = request

    def update(self):
        pass

