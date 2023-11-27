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
A member information provider is used to collect user/member/person attributes.

$Id$
"""

from zope import component
from zope.app.security.interfaces import IAuthentication
from zope.cachedescriptors.property import Lazy
from zope.interface import Interface, Attribute, implements

from cybertools.util.jeep import Jeep


# interfaces

class IMemberInfoProvider(Interface):
    """ Usually implemented by an adapter; provides a set of
        user/member/person properties.
    """

    priority = Attribute('A number denoting the priority of the provider; '
                'a provider with a high number may be overriden with a lower number.')

    data = Attribute('A collection/ordered mapping of member property objects '
                'for the currently logged-in user.')

    def getData(principalId):
        """ Return the member properties for the principal identified by
            the principal id given.
        """

    def getDataForCategory(category, principalId=None):
        """ Return a collection of the properties for the category given.
            If no principal id is given use the currently logged-in user.
        """


class IMemberProperty(Interface):

    name = Attribute('The name/identifier of the property.')
    title = Attribute('A short and descriptive title.')
    category = Attribute('A string denoting a category or classification.')


#default implementation

class MemberProperty(object):

    implements(IMemberProperty)

    def __init__(self, name, value, title=None, category='default'):
        self.name = name
        self.value = value
        self.title = title or name
        self.category = category


class MemberInfoProvider(object):

    implements(IMemberInfoProvider)

    defaultData = Jeep((MemberProperty('id', '???', u'ID'),
                        MemberProperty('title', u'unknown', u'Title'),
                        MemberProperty('description', u'',
                                       u'Description'),
                       ))

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def data(self):
        return self.getData()

    def getData(self, principalId=None):
        if principalId is None:
            principal = self.request.principal
        else:
            pau = component.getUtility(IAuthentication)
            principal = pau.getPrincipal(principalId)
        if principal is not None:
            return self.getPrincipalData(principal)
        else:
            return self.defaultData

    def getPrincipalData(self, principal):
        return Jeep((MemberProperty('id', principal.id, u'ID'),
                     MemberProperty('title', principal.title, u'Title'),
                     MemberProperty('description', principal.description,
                                    u'Description'),
                   ))
