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

"""
interface definitions for storage utilities.

$Id$
"""

from zope.interface import Interface, Attribute


class IStorageInfo(Interface):
    """ Provides information about the storage of an object.
    """

    storageName = Attribute('Name of a utility that is used for storage of the object')
    storageParams = Attribute('Dictionary with storage parameters, e.g. a '
                        'directory name')


class IExternalStorage(Interface):
    """ An external storage for data elements.
    """

    def setData(address, data, params=None):
        """ Store the data given at the address specified, using the
            (optional) params argument that may give more information on
            where and how to store the data.
        """

    def getData(address, params=None):
        """ Retrieve the data from the address specified, using the
            (optional) params argument that may give more information on
            where and how the data can be found.
        """

    # TODO: provide file and/or iterator access methods
    # read, write, close, __iter__

