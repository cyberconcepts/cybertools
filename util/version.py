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
Collect version information from different packages.
"""

revision = '$Id: version.py 3014 2008-11-28 10:56:14Z helmutm $'
version = '0.4'
package = 'cybertools.util.version'


from cybertools.util.jeep import Jeep
from cybertools.util.property import lzprop


undefined = object()
dummyRevision = '$Id$'


class Versions(dict):

    def add(self, packageName=None, versionString=None, rev=None):
        packageName = packageName or package
        versionString = versionString or version
        self[packageName] = Version(packageName, versionString, rev)

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=undefined):
        if default is undefined:
            default = Version(key, '0.0', dummyRevision)
        return super(Versions, self).get(key, default)


versions = Versions()


class Version(object):
    """ Provides the version of a package in various formats.
    """

    def __init__(self, package, versionString, rev=None):
        self.package = package
        self.versionString = versionString or version
        self.revision = rev or revision

    @lzprop
    def revparts(self):
        return self.revision.split()[2:5]

    @lzprop
    def parts(self):
        revnum, revdate, revtime = self.revparts
        return Jeep(version=self.versionTuple,
                    revnum=revnum,
                    revdate=revdate,
                    revtime=revtime,
                    revdatetime = ' '.join((revdate, revtime)),
        )

    @lzprop
    def versionTuple(self):
        return tuple(self.versionString.split('.'))

    @lzprop
    def short(self):
        return self.versionString

    @lzprop
    def long(self):
        return '%s-%s' % (self.versionString, self.parts.revnum)

    def __str__(self):
        return self.long

    def __repr__(self):
        return '%s %s' % (self.package, self.long)
