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

from zope.interface import implements
from twisted.internet import defer
#import win32com.client
#import ctypes
#import win32api, win32process, win32con
#The watsup import is needed as soon as we start handling the Outlook Pop-Up
#again
#This should also be integrated within the wrapper-api for doctests
#from watsup.winGuiAuto import findTopWindow, findControl, findControls, clickButton, \
#                              getComboboxItems, selectComboboxItem, setCheckBox

from cybertools.agent.base.agent import Agent, Master
from cybertools.agent.crawl.mail import MailCrawler
from cybertools.agent.crawl.mail import MailResource
from cybertools.agent.components import agents
from cybertools.agent.system.windows import api
from cybertools.agent.util.task import coiterate

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
                    for key in mail._prop_map_get_:
                        if isinstance(getattr(mail, key), (int, str, unicode)):
                            self.keys.append(key)
                record = {}
                for key in self.keys:
                    record[key] = getattr(mail, key)
                # Create the mime email object
                msg = self.createEmailMime(record)
                # Create a resource and append it to the result list
                self.createResource(msg, folder, "Microsoft Office Outlook")
                #return self.result
                yield None

    def login(self):
        pass

    def handleOutlookDialog(self):
        """
        This function handles the outlook dialog, which appears if someone
        tries to access to MS Outlook.
        """
        hwnd = None
        while True:
            hwnd = api.ctypes.windll.user32.FindWindowExA(None, hwnd, None, None)
            if hwnd == None:
                    break
            else:
                val = u"\0" * 1024
                api.ctypes.windll.user32.GetWindowTextW(hwnd, val, len(val))
                val = val.replace(u"\000", u"")
                if val and repr(val) == "u'Microsoft Office Outlook'":
                    print repr(val)
                    # get the Main Control
                    form = api.findTopWindow(wantedText='Microsoft Office Outlook')
                    controls = findControls(form)
                    # get the check box
                    checkBox = findControl(form, wantedText='Zugriff')
                    setCheckBox(checkBox, 1)
                    # get the combo box
                    comboBox = findControl(form, wantedClass='ComboBox')
                    items = getComboboxItems(comboBox)
                    selectComboboxItem(comboBox, items[3])#'10 Minuten'
                    # finally get the button and click it
                    button = findControl(form, wantedText = 'Erteilen')
                    clickButton(button)
                    break

    def findOutlook(self):
        outlookFound = False
        try:
            self.oOutlookApp = \
                api.client.gencache.EnsureDispatch("Outlook.Application")
            outlookFound = True
        except:
            pass
        return outlookFound

    def createEmailMime(self, emails):
        # Create the container (outer) email message.
        msg = MIMEMultipart.MIMEMultipart()
        msg['Subject'] = emails['Subject'].encode('utf-8')
        if emails.has_key('SenderEmailAddress'):
            sender = str(emails['SenderEmailAddress'].encode('utf-8'))
        else:
            sender = str(emails['SenderName'].encode('utf-8'))
        msg['From'] = sender
        recipients = []
        if emails.has_key('Recipients'):
            for rec in range(emails['Recipients'].__len__()):
                recipients.append(getattr(emails['Recipients'].Item(rec+1), 'Address'))
                msg['To'] = COMMASPACE.join(recipients)
        else:
            recipients.append(emails['To'])
            msg['To'] = COMMASPACE.join(recipients)
        msg.preamble = emails['Body'].encode('utf-8')
        return msg

agents.register(OutlookCrawler, Master, name='crawl.outlook')
