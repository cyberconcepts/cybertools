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
View class(es) for images (plots).

$Id$
"""

import os
from zope.interface import Interface, implements
from zope.cachedescriptors.property import Lazy


class PlotView(object):
    """ Abstract basic view class for Flash movies .

        The assessment attribute has to be set by the subclass.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def __call__(self):
        if self.traverse_subpath:
            path = str('/' + os.path.join(*self.traverse_subpath))
        else:
            path = self.request.form.get('image')
        # TODO: keep path in temporary dictionary with hashed keys.
        self.setHeaders(path)
        f = open(path, 'rb')
        data = f.read()
        f.close()
        return data

    def setHeaders(self, name=None):
        response = self.request.response
        # TODO: get content type from name (extension)
        response.setHeader('Content-Type', 'image/jpeg')
        response.setHeader('Expires', 'Sat, 1 Jan 2000 00:00:00 GMT');
        response.setHeader('Pragma', 'no-cache');

