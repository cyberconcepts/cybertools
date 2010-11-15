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
View controller for the Lobo skin.

$Id$
"""

from cybertools.browser.controller import Controller as BaseController


class Controller(BaseController):

    def __init__(self, context, request):
        self.view = view = context         # the controller is adapted to a view
        self.context = context.context
        self.request = request
        self.setupCss()
        self.setupJs()
        super(Controller, self).__init__(context, request)

    def setupCss(self):
        macros = self.macros
        presentationMode = self.request.get('liquid.viewmode') == 'presentation'
        params = [('blue/blue8.css', 'all', 20, False),
                  ('print.css', 'print', 25, False),
                  ('blue/blueprint/ie.css', 'all', 30, True),
                  ('custom.css', 'all', 100, False)]
        #if presentationMode:
        #    params.append(('presentation.css', 'all', 30, False))
        for id, media, prio, ie in params:
            macros.register('css', identifier=id, resourceName=id, media=media,
                            priority=prio, is_ie=ie)

    def setupJs(self):
        return
