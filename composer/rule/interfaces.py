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
Message management.

$Id$
"""

from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
from zope import schema

from cybertools.composer.interfaces import ITemplate, IComponent

_ = MessageFactory('zope')


class IRuleManager(Interface):
    """ A manager (or container) for rules.
    """

    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title of the object.'),
                required=True,)

    rules = Attribute('An ordered collection of rules managed by this object.')

    def handleEvent(event):
        """ Handle the event given and apply the corresponding rules
            to the client object.
        """


class IRule(ITemplate):
    """ A rule that will be applied .
    """

    name = schema.ASCII(
                title=_(u'Name'),
                description=_(u'The internal name of the rule.'),
                required=True,)
    title = schema.TextLine(
                title=_(u'Title'),
                description=_(u'The title or label of the rule.'),
                required=True,)
    description = schema.Text(
                title=_(u'Description'),
                description=_(u'A brief description of the rule.'),
                required=False,)

    manager = Attribute('The associated rule manager.')
    events = Attribute('The events to be handled by this rule.')
    conditions = Attribute('Conditions to be checked.'
                'This is typically a list of names of ICondition adapters.')
    actions = Attribute('Sequence of actions to be carried out by this rule.')


class IEvent(Interface):

    name = Attribute('The name by which the event will be identified.')
    title = Attribute('A human readable title or label.')
    context = Attribute('An object that is associated with the event.')


class ICondition(Interface):

    def __call__(context, params):
        """ Should return True if the condition should be fulfilled;
            will allow the rule to call its actions.
        """


class IAction(IComponent):
    """ Controls what will be done.
    """

    name = schema.ASCII(
                title=_(u'Name'),
                description=_(u'The name of the action.'),
                required=True,)

    handlerName = Attribute('Name of the adapter that will carry out the action.')
    parameters = Attribute('Mapping with additional preset informations that '
                'will be supplied to the action handlers.')
    rule = Attribute('The rule the action belongs to.')


class IActionHandler(Interface):
    """ Does the real work.
    """

    def __call__(data, params):
        """ Execute the action, using the data and parameters given (mappings).
        """

