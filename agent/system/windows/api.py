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
Conficuration-controlled import of Windows API functions.

$Id$
"""

def setup(config):
    global client, ctypes, win32api, win32process, win32con
    if config.system.winapi == 'testing':
        from cybertools.agent.testing.winapi import \
                        client, ctypes, win32api, win32process, win32con
    else:
        try:
            from win32com import client
            import ctypes
            import win32api, win32process, win32con
        except ImportError:
            from cybertools.agent.testing.winapi import \
                        client, ctypes, win32api, win32process, win32con

