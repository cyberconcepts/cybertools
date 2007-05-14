#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Service instance classes.

$Id$
"""

from zope.interface import implements

from cybertools.organize.interfaces import IService
from cybertools.organize.interfaces import IScheduledService


class Registration(object):

    def __init__(self, client):
        self.client = client


class Service(object):

    implements(IService)

    def __init__(self, seats=-1):
        self.capacity = capacity
        self.registrations = []

    @property
    def availableCapacity(self):
        if self.capacity >= 0 and len(self.registrations) >= self.capacity:
            return 0
        return self.capacity - len(self.registrations)

    def register(self, client):
        if self.availableCapacity:
            reg = Registration(client)
            self.registrations.append(reg)
            return reg
        return None


class ScheduledService(Service):

    implements(IScheduledService)
