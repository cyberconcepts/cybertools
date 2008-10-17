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
Controller that receives and responds to requests from a browser (AJAX) client;
in parallel it sends  informations to the client by responding to
polling requests from the client.

$Id$
"""

from zope.interface import implements

from cybertools.agent.base.agent import Master
from cybertools.agent.core.control import SampleController
from cybertools.agent.components import controllers


class ClientController(SampleController):

    def setup(self):
        super(ClientController, self).setup()


controllers.register(ClientController, Master, name='ajaxclient')
