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
Fake testing objects/functions for HTTP communication.

$Id$
"""

from twisted.internet.defer import Deferred, succeed


class Listener(object):

    site = port = None

    def listenTCP(self, port, site):
        self.port = port
        self.site = site
        self.resource = site.resource
        deferred = self.deferred = Deferred()
        return deferred


listener = Listener()


def getPage(url, contextFactory=None, method='GET', postdata=None, **kwargs):
    return succeed('{"message": "OK"}')
