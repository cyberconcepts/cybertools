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
A set of simple application classes for contact management; this may be used
as an example for some of the cybertools packages, but may also be the base
for some real life stuff.

$Id$
"""

from zope.interface import implements
from datetime import date
from cybertools.organize.interfaces import IPerson, IAddress


class Person(object):

    implements(IPerson)
    
    def __init__(self, lastName, firstName=u'', birthDate=None):
        self.lastName = lastName
        self.firstName = firstName
        self.birthDate = birthDate
        self.moreFirstNames = None
        self.personalAddress = 'mrs' # or 'mr', 'ms', None (unknown)
        self.academicTitle = None
        self.communicationInfos = []
        self.addresses = {}         # keys: 'standard', ...?
        self.affiliations = {}      # keys: 'employed', ...?

    @property
    def age(self):
        return self.ageAt(date.today())

    def ageAt(self, date):
        if self.birthDate is None:
            return None
        return int((date - self.birthDate).days/365.25)


class Address(object):

    implements(IAddress)

    def __init__(self, city, street=u'', lines=[],
                 zipcode=None, country=None):
        self.lines = lines      # a sequence of additional address lines
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.country = country  # 'de', 'at', 'us', ...


class Institution(object):

    def __init__(self, title):
        self.title = title
        self.addresses = {}


class CommunicationInfo(object):

    def __init__(self, commType, qualifier, address):
        self.commType = commType    # e.g. 'email', 'phone', ...
        self.qualifier = qualifier  # e.g. 'private', or institution
        self.address = address      # the real address or number

