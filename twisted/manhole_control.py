##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Manhole Control View

$Id$
"""
__docformat__ = 'restructuredtext'

from cybertools.twisted import manhole

class ManholeControlView(object):

    def isOpen(self):
        return manhole.listener is not None

    def toggleState(self):
        if self.isOpen():
            manhole.close()
        else:
            manhole.open(self.port(), self.request)

    def port(self):
        return manhole.port

    def update(self):
        if not self.request.get('form_submitted'):
            return
        port = self.request.get('manhole.port')
        if port:
            manhole.port = int(port)
        if self.request.get('manhole.setting', False):
            self.toggleState()
