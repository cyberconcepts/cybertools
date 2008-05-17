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
Module for handling Outlook dialoges
$Id$
"""

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