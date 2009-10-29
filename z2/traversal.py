#
#  Copyright (c) 2009 Helmut Merz - helmutm@cy55.de
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
IPublishTraverse adapter for Zope 2 objects providing IBase.

$Id$
"""

from zope import component
from ZPublisher.BaseRequest import DefaultPublishTraverse
from ZPublisher.HTTPRequest import HTTPRequest

from cybertools.util.generic.interfaces import IGeneric


class Traverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        typeInterface = getattr(self.context, 'typeInterface', None)
        if typeInterface is not None:
            genObj = IGeneric(self.context, None)
            if genObj is not None:
                obj = typeInterface(genObj, None)
                if obj is not None:
                    view = component.queryMultiAdapter((obj, request), name=name)
                    #print '*** obj', obj, view
                    if view is not None:
                        return view
        return super(Traverser, self).publishTraverse(request, name)

