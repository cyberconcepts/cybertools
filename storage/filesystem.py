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
Storing data in files in the file system.

$Id$
"""

import os
import cybertools
from zope.interface import implements
from cybertools.storage.interfaces import IExternalStorage

DEFAULT_DIRECTORY = 'extfiles'


class FileSystemStorage(object):

    implements(IExternalStorage)

    def __init__(self, rootDir, subDir):
        self.rootDir = rootDir
        self.subDir = subDir

    def getDir(self, address, subDir=None):
        subDir = subDir or self.subDir
        return os.path.join(self.rootDir, subDir, address)

    def setData(self, address, data, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        f = open(fn, 'wb')
        f.write(data)
        f.close()
        print 'cybertools.storage: file %s written' % fn

    def getData(self, address, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        f = open(fn, 'rb')
        data = f.read()
        f.close()
        return data


def explicitDirectoryStorage(dirname):
    """ This cannot be used as a utility but must be called explicitly."""
    return FileSystemStorage('', dirname)


def instanceVarSubdirectoryStorage(dirname=DEFAULT_DIRECTORY):
    instanceHome = os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.dirname(cybertools.__file__))))
    varDir = os.path.join(instanceHome, 'var');
    return FileSystemStorage(varDir, dirname)
