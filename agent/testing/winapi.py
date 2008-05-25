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
Fake Windows API functions for testing purposes.

$Id$
"""

win32api = win32process = win32con = None


class com_error(Exception):
    pass


class Attachments(list):
    
    elemCount = 0
    data = []

    def __init__(self, files=[]):
        for elem in files:
            fileitem = Attachment(filename=elem)
            self.data.append(fileitem)
            print "Attachment: ", fileitem.FileName

    @property
    def Application(self):
        print "Outlook application instance"
        return "Outlook application instance"
    
    def Item(self, index):
        return self.data[index-1]
    
    @property
    def count(self):
        print self.elemCount
        return self.elemCount
    
##    @property
##    def Data(self):
##        return self.elemList
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        yield self.data
        
    def __getitem__(self, idx):
        return self.data[idx]

    
class Attachment(object):
    
    File = ""
    
    def __init__(self, filename=""):
        self.File = filename
    
    def SaveAsFile(self, path=""):
        print "Attachment saved"
    
    @property
    def Parent(self):
        # return value of Attribute Parent is of type _MailItem
        pass
    
    @property
    def Type(self):
        pass
    
    @property
    def Size(self):
        # the size property is not available in Outlook 2000
        pass
    
    @property
    def Application(self):
        # Actual instance of Outlook application
        pass
    
    @property
    def FileName(self):
        return self.File
    
    
class Mail(object):

    #this is just a guess what a Outlook Mail Object Probably returns
    #Class = client.constants.olMail

    def __init__(self, subj="", sendName="", to="", body="", **kw):
        self.Class = client.constants.olMail
        self.Subject = subj
        self.SenderName = sendName
        self.To = to
        self.Body = body
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def _prop_map_get_(self):
        #here it is necessary of what attributes (called keys in outlok.py)
        #an Outlook Mail typically has
        return self.__dict__


class Items(object):

    def __init__(self):
        self.data = {}
        self.data[0] = Mail(Subject="Python Training",
                            SenderName="Mark Pilgrim",
                            To="allPythonics@python.org",
                            Body="The training will take place on Wed, 21st Dec.\
                                  Kindly check the enclosed invitation.",
                            BodyFormat=1,
                            Attachments=Attachments(["Invitation.pdf", "21.pdf"])
                            )
        self.data[1] = Mail()
        self.data[2] = Mail()

    def Item(self, idx):
        return self.data[idx-1]

    def __len__(self):
        return len(self.data)


class OutlookFolder(object):

    # Folders defines in Outlook the sub folders under the "Main" Folder
    Folders = None

    def __init__(self):
        print "collecting Mails from folder"
        self.Items = Items()


class OutlookNamespace(object):

    def __init__(self):
        pass

    def GetDefaultFolder(self, message=""):
        print "retrieving Outlook default folder"
        folder = OutlookFolder()
        return folder


class OutlookApp(object):

    def __init__(self):
        pass

    def GetNamespace(self, message=""):
        print "Namespace " + message + " retrieved"
        oNamespace = OutlookNamespace()
        return oNamespace


class Message(object):

    olFolderInbox = None
    # esp. for olMail, for further dummy implementations it is necessary
    # to find out, what class is expected. Meaning what type of object has
    # to be faked and what attributes it has. see outlook.py
    # loadMailsfromFolder
    olMail = Mail

    def __init__(self):
        pass

    def EnsureDispatch(self, message=""):
        print message + " retrieved"
        oApp = OutlookApp()
        return oApp


class client(object):

    gencache = Message()
    constants = Message()

    def __init__(self):
        pass

class ctypes(object):

    def __init__(self):
        pass