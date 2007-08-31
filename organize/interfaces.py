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
Interfaces for organizational stuff like persons, addresses, tasks, services...

$Id$
"""

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory

from cybertools.util.jeep import Jeep, Term

_ = MessageFactory('zope')


# schema fields

class SimpleList(schema.List): pass

class LinesList(schema.List): pass


# persons, addresses, ...

class IPerson(Interface):
    """ Resembles a human being with a name (first and last name),
        a birth date, and a set of addresses.
    """

    firstName = schema.TextLine(
                    title=_(u'First name'),
                    description=_(u'The first name'),
                    required=False,)
    lastName = schema.TextLine(
                    title=_(u'Last name'),
                    description=_(u'The last name or surname'),)
    email = schema.TextLine(
                    title=_(u'E-Mail address'),
                    description=_(u'The standard email address of the person'),)
    phoneNumbers = SimpleList(
                    value_type=schema.TextLine(),
                    default=[],
                    title=_(u'Phone numbers'),
                    description=_(u'Note one or more phone numbers here'),
                    required=False,)
    birthDate = schema.Date(
                    title=_(u'Date of birth'),
                    description=_(u'The date of birth - should be a '
                                   'datetime.date object'),
                    required=False,)

    age = schema.Int(
                    title=_(u'Age'),
                    description=_(u'The current age in full years'),
                    readonly=True)

    addresses = Attribute('A mapping whose values provide the IAddress '
                          'interface')


class IAddress(Interface):
    """ A postal address of a person or institution.
    """

    street = schema.TextLine(
                    title=_(u'Street, number'),
                    description=_(u'Street and number'),
                    required=False,)
    zipcode = schema.TextLine(
                    title=_(u'ZIP code'),
                    description=_(u'ZIP code, postal code'),
                    required=False,)
    city = schema.TextLine(
                    title=_(u'City'),
                    description=_(u'Name of the city'),
                    required=True,)
    country = schema.TextLine(
                    title=_(u'Country code'),
                    description=_(u'International two-letter country code'),
                    required=False,)
    lines = LinesList(
                    value_type=schema.TextLine(),
                    default=[],
                    title=_(u'Additional lines'),
                    description=_(u'Additional address lines'),
                    required=False,)


# tasks

class ITask(Interface):
    """ A task has a start date, an optional end date, and is usually
        assigned to one or more persons.
    """

    start = schema.Date(
                    title=_(u'Start date'),
                    description=_(u'The date when the task should start'),
                    required=False,)
    end = schema.Date(
                    title=_(u'End date'),
                    description=_(u'The date until that the task should be '
                                   'finished'),
                    required=False,)


# services

serviceManagerViews = SimpleVocabulary((
    SimpleTerm('', '', u'Default view'),
    SimpleTerm('events_overview.html', 'events_overview.html', u'Events overview'),
))

class IServiceManager(Interface):
    """ A manager or container for a set of services.
    """

    start = schema.Date(
                title=_(u'Start date/time'),
                description=_(u'The start date/time for providing services.'),
                required=False,)
    end = schema.Date(
                title=_(u'End date/time'),
                description=_(u'The end date/time for providing services.'),
                required=False,)
    viewName = schema.Choice(
                title=_(u'View name'),
                description=_(u'Select the name of a specialized view to be used '
                        'for presenting this object.'),
                vocabulary=serviceManagerViews,
                default='',
                required=False,)

    services = Attribute('A collection of services managed by this object.')


class IServiceGroup(Interface):
    """ A group of related services or a general service definition,
        e.g. a regular bus service or a series of trainings.
    """

    services = Attribute('A collection of services belonging to this object.')


serviceCategories = SimpleVocabulary((
    SimpleTerm('event', 'event', u'Event'),
    SimpleTerm('transport', 'transport', u'Transport'),
))

class IService(Interface):
    """ A service that clients may register with.
    """

    title = Attribute('A descriptive but short title')

    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the item.'),
                required=False,)
    category = schema.Choice(
                title=_(u'Category'),
                description=_(u'The type of '
                        'this service, e.g. an event or a transport.'),
                vocabulary=serviceCategories,
                default='event',
                required=False,)
    capacity = schema.Int(
                title=_(u'Capacity'),
                description=_(u'The capacity (maximum number of clients) '
                        'of this service; a negative number means: '
                        'no restriction, i.e. unlimited capacity.'),
                required=False,)
    availableCapacity = Attribute('Available capacity, i.e. number of seats '
                'still available; a negative number means: '
                'no restriction, i.e. unlimited capacity; '
                'read-only')

    token = Attribute('A name unique within the manager of this service '
                'used for identifying the service e.g. in forms.')
    serviceGroup = Attribute('The service group this object is an instance of.')
    classification = Attribute('A sequence of tokenized terms characterizing '
                'this service within a hierarchy of concepts.')

    serviceProviders = Attribute('A collection of one or more service providers.')
    resources = Attribute('A collection of one or more resources.')
    registrations = Attribute('A collection of client registrations.')

    def register(client):
        """ Register a client with this service. Return an IRegistration
            object if the registration is successful, otherwise
            (e.g. if the service's capacity is exhausted) return None.
        """

    def unregister(client):
        """ Remove the client from this service's registrations.
        """


class IScheduledService(IService):
    """ A service that starts at a certain date/time and
        usually ends a certain time later.
    """

    start = schema.Date(
                title=_(u'Start date/time'),
                description=_(u'The date/time when the service starts'),
                required=False,)
    start.default_method = 'getStartFromManager'
    end = schema.Date(
                title=_(u'End date/time'),
                description=_(u'The date/time when the service ends'),
                required=False,)
    end.default_method = 'getEndFromManager'
    duration = Attribute('Time delta between start and end date/time.')


class IClient(Interface):
    """ An fairly abstract interface for objects to be used as clients
        for services.
    """

    manager = Attribute('The object that cares for this client.')


class IClientFactory(Interface):
    """ Creates client objects.
    """

    def __call__(data):
        """ Creates and returns a client object built from the
            data set provided.
        """


class IRegistration(Interface):
    """ Information about the registration of a client with a service.
    """

    client = Attribute('The client registered')


class IRegistrationTemplate(Interface):
    """ A content object controlling access to service registrations
        of a certain client.

        The client should be accessed via an IClientRegistrations adapter.
    """

    # TODO: provide fields for criteria for selecting the services
    #       that should be handled by this object, e.g. service
    #       category/ies or classification(s).

    manager = Attribute('The service manager this object belongs to.')
    services = Attribute('A collection of services to which this '
                'object provides access. This may be all or part '
                'of the services managed by the manager.')


class IClientRegistrations(Interface):
    """ Provides access to a client object and allows to manage its service
        registrations.
    """

    template = Attribute('A regstration template that is used '
                'for controlling the registration process.')

    def register(services):
        """ Register the client for the services given.
        """

    def unregister(services):
        """ Remove the client from the services given.
        """

    def getRegistrations():
        """ Return the client's service registrations.
        """


class IResource(Interface):
    """ A resource is needed by a service to be able to work, e.g. a
        room or a bus. A resource may have a limited capacity so that
        at a certain time it may only be used by services to a certain
        extent.
    """


class IServiceProvider(Interface):
    """ A party, that is responsible for providing a service.
    """

