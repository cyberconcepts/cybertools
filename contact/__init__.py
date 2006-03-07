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
A set of simple application classes for contact management to be used
as an example for some of the cybertools packages.

$Id$
"""

from zope.component import adapts
from zope.interface import implements
from cybertools.contact.interfaces import IPerson
from datetime import date


class Person(object):

    implements(IPerson)
    
    def __init__(self, firstName, lastName, birthDate):
        self.firstName = firstName
        self.lastName = lastName
        self.birthDate = birthDate
        self.moreFirstNames = []
        self.personalAddress = 'mrs' # or 'mr', 'ms', None (unknown)
        self.academicTitle = None
        self.communicationInfos = []
        self.addresses = {}         # keys: 'standard', ...?
        self.affiliations = {}      # keys: 'employed', ...?

    @property
    def age(self):
        return (date.today() - self.birthDate).days/365.25


class Address(object):

    def __init__(self, title, lines, street, zipcode, city, country):
        self.title = title
        self.lines = lines      # a sequence of address lines
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

