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

client = ctypes = win32api = win32process = win32con = None

class Mail(object):
    
    #this is just a guess what a Outlook Mail Object Probably returns
    Class = None

    def __init__(self):
        Class = self.__class__
    
    def _prop_map_get_(self):
        #here it is necessary of what attributes (called keys in outlok.py)
        #an Outlook Mail typically has
        # should return a tuple ()
        pass
    

class OutlookFolder(object):
    
    Items = {}
    # Folders defines in Outlook the sub folders under the "Main" Folder
    Folders = None
    
    def __init__(self):
        Items[0] = Mail()
        Items[1] = Mail()
        pass


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
    olMail = Mail()
    
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