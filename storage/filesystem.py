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

from datetime import datetime
from logging import getLogger
import os
import shutil
from zope.interface import implements
import transaction
from transaction.interfaces import IDataManager

import cybertools
from cybertools.storage.interfaces import IExternalStorage

DEFAULT_DIRECTORY = 'extfiles'


logger = getLogger('cybertools.storage.filesystem')


class FileSystemStorage(object):

    implements(IExternalStorage)

    def __init__(self, rootDir=None, subDir=None):
        self.rootDir = rootDir
        self.subDir = subDir

    def getDir(self, address, subDir=None):
        subDir = subDir or self.subDir
        if self.rootDir is None:
            if subDir:
                return os.path.join(subDir, address)
            return address
        return os.path.join(self.rootDir, subDir, address)

    def setData(self, address, data, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        directory = os.path.dirname(fn)
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(fn, 'wb')
        f.write(data)
        f.close()
        #print 'cybertools.storage: file %s written' % fn
        # TODO: transaction management:
        # write to temp file in subDir, keep address in internal dictionary
        # transaction.manager.get().join(FSSDataManager(address, temp))
        # then rename in tpc_finish() and remove temp file in tpc_abort

    def getData(self, address, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        #print '***', [self.rootDir, subDir, address], fn
        try:
            f = open(fn, 'rb')
            data = f.read()
            f.close()
            return data
        except IOError, e:
            logger.warn(e)
                        #'File %r cannot be read.' % fn)
            return ''

    def getSize(self, address, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        try:
            return os.path.getsize(fn)
        except OSError, e:
            logger.warn(e)
            return 0

    def getMTime(self, address, params={}):
        subDir = params.get('subdirectory')
        fn = self.getDir(address, subDir)
        try:
            ts = os.path.getmtime(fn)
            if ts:
                return datetime.fromtimestamp(ts)
        except OSError, e:
            logger.warn(e)
            return None

    def getUniqueAddress(self, address, params={}):
        subDir = params.get('subdirectory')
        return self.getDir(address, subDir)

    def copyDataFile(self, sourceAddress, sourceParams, targetAddress, targetParams):
        source = self.getDir(sourceAddress, sourceParams.get('subdirectory'))
        target = self.getDir(targetAddress, targetParams.get('subdirectory'))
        targetDir = os.path.dirname(target)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        shutil.copyfile(source, target)



class FSSDataManager(object):

    implements(IDataManager)

    transaction_manager = None

    def __init__(self, address, temp):
        self.address = address
        self.temp = temp
        self.transaction_manager = transaction.manager

    def abort(self, transaction):
        # remove temp file
        pass

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        # rename original file if present to a temporary name
        # rename temp file to original name
        pass

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        # remove renamed original file
        pass

    def tpc_abort(self, transaction):
        # rename back original file (removing renamed temp file)
        pass

    def sortKey(self):
        return 'cybertools.storage.FileSystemStorage:' + self.address


def explicitDirectoryStorage(dirname):
    """ This cannot be used as a utility but must be called explicitly."""
    return FileSystemStorage('', dirname)


def fullPathStorage():
    return FileSystemStorage()


def instanceVarSubdirectoryStorage(dirname=DEFAULT_DIRECTORY):
    instanceHome = os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.dirname(cybertools.__file__))))
    varDir = os.path.join(instanceHome, 'var');
    return FileSystemStorage(varDir, dirname)
