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
Interfaces for handling asynchronous communication tasks.

$Id$
"""

from zope.interface import Interface, Attribute


class IServer(Interface):
    """ A server waits for connection requests from a client. A connected
        client may then send data to or receive messages from the server.
    """

    def subscribe(subscriber, aspect):
        """ The subscriber will receive messages via its ``onMesssage`` method.

            The aspect is a dotted string used to select the kind of
            sessions/remote clients the subscriber wants to receive messages
            from.
        """

    def unsubscribe(subscriber, aspect):
        """ Stop receiving messages.
        """

    def send(session, data, interaction=None):
        """ Send data to the remote client specified via the session given.
            The session has to be created previously by a connect attempt
            from the client.

            If interaction is None, create a new one.
            Return the interaction.
        """


class IClient(Interface):
    """ A client initiates a connection (session) to a server and may then
        sent data to or receive data from the server.
    """

    def connect(subscriber, url, credentials=None):
        """ Connect to a server using the URL given, optionally logging in
            with the credentials given.

            The subscriber will receive messages via its ``onMesssage`` callback.

            Return a an ISession implementation that may be used for sending
            data to the server.
        """

    def disconnect(session):
        """ Close the connection for the session given.
        """

    def send(session, data, interaction=None):
        """ Send data to the server specified via the session given.

            If interaction is None, create a new one.
            Return the interaction.

            Sending an interaction with ``finished`` set to True signifies
            the last message of an interaction.
        """


# auxiliary interfaces

class ISubscriber(Interface):
    """ May receive message notifications.
    """

    def onMessage(interaction, data):
        """ Callback method for message notifications.
        """

    def onError(interaction, data):
        """ Callback method for error notifications.
        """


class ISession(Interface):
    """ Represents the connection to a server within a client or
        a remote client connection within a server.
    """

    manager = Attribute("""The server or client object, respectively, that
                created the session.""")
    subscriber = Attribute("The subscriber that initiated the session.")
    url = Attribute("The URL of the server (or client) the session connects to.")
    state = Attribute("""A string specifying the current state of the session:
                'logon': The remote client is trying to connect/log in,
                         data may contain credential information;
                'logoff': The remote client is closing the connection;
                'open': The connection is open.""")


class IInteraction(Interface):
    """ Represents a set of message exchanges belonging together.
    """

    session = Attribute("The session the interaction belongs to.")
    finished = Attribute("The interaction is finished, interaction data may be cleared.")
