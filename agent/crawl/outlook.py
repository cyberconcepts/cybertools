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
Outlook Crawler Class.

$Id$
"""

import re
from email import MIMEMultipart
import tempfile
import os

from zope.interface import implements
from twisted.internet import defer
#from pywintypes import com_error
#The watsup import is needed as soon as we start handling the Outlook Pop-Up
#again
#This should also be integrated within the wrapper-api for doctests
#from watsup.winGuiAuto import findTopWindow, findControl, findControls, clickButton, \
#                              getComboboxItems, selectComboboxItem, setCheckBox

from cybertools.agent.base.agent import Agent, Master
from cybertools.agent.crawl.mail import MailCrawler
from cybertools.agent.crawl.mail import MailResource
from cybertools.agent.crawl.filesystem import FileResource
from cybertools.agent.components import agents
from cybertools.agent.system.windows import api
from cybertools.agent.util.task import coiterate
from cybertools.agent.system.windows.codepages import codepages

# some constants
COMMASPACE = ', '

class OutlookCrawler(MailCrawler):

    keys = ""
    inbox = ""
    subfolders = ""
    pattern = ""

    def collect(self, filter=None):
        self.result = []
        self.d = defer.Deferred()
        self.oOutlookApp = None
        if self.findOutlook():
            self.fetchCriteria()
            coiterate(self.crawlFolders()).addCallback(self.finished).addErrback(self.error)
        else:
            pass
            #self.d.addErrback([])
        return self.d

    def error(self, reason):
        print '***** error',
        print reason

    def finished(self, result):
        self.d.callback(self.result)

    def fetchCriteria(self):
        criteria = self.params
        self.keys = criteria.get('keys')
        self.inbox = criteria.get('inbox') #boolean
        self.subfolders = criteria.get('subfolders') #boolean
        self.pattern = criteria.get('pattern')
        if self.pattern != '' and self.pattern != None:
            self.pattern = re.compile(criteria.get('pattern') or '.*')

    def crawlFolders(self):
        onMAPI = self.oOutlookApp.GetNamespace("MAPI")
        ofInbox = \
            onMAPI.GetDefaultFolder(api.client.constants.olFolderInbox)
        # fetch mails from inbox
        if self.inbox:
            for m in self.loadMailsFromFolder(ofInbox):
                yield None
        # fetch mails of inbox subfolders
        if self.subfolders and self.pattern is None:
            lInboxSubfolders = getattr(ofInbox, 'Folders')
            for of in range(lInboxSubfolders.__len__()):
                # get a MAPI-subfolder object and load its emails
                for m in self.loadMailsFromFolder(lInboxSubfolders.Item(of + 1)):
                    yield None
        elif self.subfolders and self.pattern:
            lInboxSubfolders = getattr(ofInbox, 'Folders')
            for of in range(lInboxSubfolders.__len__()):
                # get specified MAPI-subfolder object and load its emails
                if self.pattern.match(getattr(lInboxSubfolders.Item(of + 1), 'Name')):
                    for m in self.loadMailsFromFolder(lInboxSubfolders.Item(of + 1)):
                        yield None

    def loadMailsFromFolder(self, folder):
        # get items of the folder
        folderItems = getattr(folder, 'Items')
        for item in range(len(folderItems)):
            mail = folderItems.Item(item+1)
            if mail.Class == api.client.constants.olMail:
                if self.keys is None:
                    self.keys = []
                    for key in mail._prop_map_get_.items():
                        try:
                            if isinstance(key[0], (int, str, unicode, bool)):
                                self.keys.append(key[0])
                        except api.com_error:
                            pass
                record = {}
                for key in self.keys:
                    try:
                        if (hasattr(mail, key)):
                            value = getattr(mail, key)
                            if isinstance(value, (int, str, unicode, bool)):
                                record[key] = value
                            else:
                                record[key] = None
                    except:
                        pass
                metadata = self.assembleMetadata(folder, record)
                # Create a resource and append it to the result list
                self.createResource(mail, folder, metadata)
                yield None

    def findOutlook(self):
        outlookFound = False
        try:
            self.oOutlookApp = \
                api.client.gencache.EnsureDispatch("Outlook.Application")
            outlookFound = True
        except com_error:
            pass
        return outlookFound

    def assembleMetadata(self, folder, mailAttr):
        meta = {}
        for key in mailAttr.keys():
            if isinstance(mailAttr[key], (str, unicode))\
               and mailAttr[key] != 'Body' and mailAttr[key] != 'HTMLBody':
                meta[key] = mailAttr[key].encode('utf-8')
            elif isinstance(mailAttr[key], (list, tuple, dict)):
                lst = []
                for rec in mailAttr[key]:
                    lst.append(rec)
                    meta[key] = COMMASPACE.join(lst)
            else:
                meta[key] = mailAttr[key]
        meta["path"] = folder
        metadata = self.createMetadata(meta)
        return metadata
    
    def createResource(self, mail, folder, metadata):
        enc = None
        textType = "application/octet-stream"
        attachments = []
        mailContent = ""
        ident = None
        if (hasattr(mail, 'BodyFormat')):
            value = getattr(mail, 'BodyFormat')
            if value == 1:
                #1: it is a plain text mail, that is maybe decorated with
                #some html Tags by Outlook for formatting
                #so save it as plain text mail
                if hasattr(mail, 'Body'):
                    mailContent = getattr(mail, 'Body')
                    textType = "text/plain"
                else:
                    mailContent = ""
                    textType = "text/plain"
            elif value == 2:
                #2: it is a HTML mail
                if hasattr(mail, 'HTMLBody'):
                    mailContent = getattr(mail, 'HTMLBody')
                    textType = "text/html"
                else:
                    mailContent = ""
                    textType = "text/html"
        else:
            #Could not determine BodyFormat. Try to retrieve plain text
            if hasattr(mail, 'Body'):
                mailContent = getattr(mail, 'Body')
            else:
                mailContent = ""
        if hasattr(mail, 'InternetCodepage'):
            Codepage = getattr(mail, 'InternetCodepage')
            if codepages.has_key(Codepage):
                enc = codepages[Codepage]
        if hasattr(mail, 'EntryID'):
            ident = getattr(mail, 'EntryID')
        if hasattr(mail, 'Attachments'):
            attachedElems = getattr(mail, 'Attachments')
            for item in range(1, len(attachedElems)+1):
                fileHandle, filePath = tempfile.mkstemp(prefix="outlook")
                attachedItem = attachedElems.Item(item)
                attachedItem.SaveAsFile(filePath)
                os.close(fileHandle)
                metadat = self.createMetadata(dict(filename=filePath))
                fileRes = FileResource(data=None,
                                       path=filePath,
                                       metadata=metadat)
                attachments.append(fileRes)
        fileHandle, filePath = tempfile.mkstemp(prefix="olmail")
        filePointer = os.fdopen(fileHandle, "w")
        mailContent = mailContent.encode('utf-8')
        filePointer.write(mailContent)
        filePointer.close()
        resource = MailResource(data=mailContent,
                                contentType=textType,
                                encoding=enc,
                                path=filePath,
                                application='outlook',
                                identifier=ident,
                                metadata=metadata,
                                subResources=attachments)
        self.result.append(resource)

agents.register(OutlookCrawler, Master, name='crawl.outlook')
