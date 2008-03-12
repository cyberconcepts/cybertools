#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
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
External content integration interfaces.

$Id$
"""

from zope.app.container.interfaces import IReadContainer
from zope.app.file.interfaces import IFile, IImage
from zope.app.publication.interfaces import IFileContent
from zope.interface import Interface, Attribute


class IFile(IFile, IFileContent):

    def getData(num):
        """ Return num bytes from the file`s data.
        """


class IProxyFactory(Interface):
    """ Creates proxy objects for external objects.
    """

    def __call__(address, **kw):
        """ Return a proxy object based on an external object that
            can be accessed using the address (and optional
            keyword arguments) given.
        """


class IContainerFactory(IProxyFactory):
    """ Creates container proxy objects for the external specification
        given.
    """


class IFileFactory(IProxyFactory):
    """ Creates file proxy objects for the external specification
        given.
    """

