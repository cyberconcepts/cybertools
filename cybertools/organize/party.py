# cybertools.organize.party

""" A set of simple application classes for contact management; this may be used
as an example for some of the cybertools packages, but may also be the base
for some real life stuff.
"""

from zope.interface import implementer
from datetime import date
from cybertools.organize.interfaces import IPerson, IAddress


@implementer(IPerson)
class Person(object):

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

    def ageAt(self, dt):
        bd = self.birthDate
        if not bd:
            return None
        return int((dt - date(bd.year, bd.month, bd.day)).days/365.25)


@implementer(IAddress)
class Address(object):

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

