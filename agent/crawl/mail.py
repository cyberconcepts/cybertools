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
Crawl base and sample classes.

$Id$
"""

from zope.interface import implements

from cybertools.agent.base.agent import Agent, Master
from cybertools.agent.crawl.base import Resource
from cybertools.agent.crawl.base import Crawler
from cybertools.agent.components import agents
from twisted.internet.defer import succeed


class MailCrawler(Crawler):

    def __init__(self, params):
        self.params = params
        self.result = []

    def collect(self, filter=None):
        print 'MailCrawler is collecting.'
        # d = self.crawlFolders()
        d = succeed([])
        return d
    
    def fetchCriteria(self):
        pass

    def crawlFolders(self):
        pass

    def loadMailsFromFolder(self, folder):
        pass

    def createResource(self, mail, path="", application="", metadata=None):
        resource = MailResource(mail, path, application, metadata)
        self.result.append(resource)

    def login(self):
        pass


class MailResource(Resource):
    pass

agents.register(MailCrawler, Master, name='crawl.mail')