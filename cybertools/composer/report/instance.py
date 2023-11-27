#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Report instance and related classes.

$Id$
"""

from string import Template
from zope import component
from zope.interface import implements
from zope.publisher.browser import TestRequest
try:
    from zope.traversing.browser.absoluteurl import absoluteURL
    zope29 = False
except ImportError:
    from zope.app.traversing.browser.absoluteurl import absoluteURL
    from Acquisition import aq_parent, aq_inner
    zope29 = True

from cybertools.composer.instance import Instance
from cybertools.composer.interfaces import IInstance
from cybertools.util.jeep import Jeep

_not_found = object()


class ReportInstance(Instance):

    template = client = None

    def __init__(self, client, template, manager):
        self.client = client
        self.template = template
        self.manager = manager

    def applyTemplate(self, **kw):
        data = []   # TODO: create result set
        request = data.get('request') or TestRequest()
        return data

