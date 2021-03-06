#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
View classes for reports.

$Id$
"""

from zope import interface, component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy

from cybertools.reporter.resultset import ResultSet
from loops.browser.common import BaseView


reportMacros = ViewPageTemplateFile('macros.pt')


class DetailView(BaseView):

    template = reportMacros

    @Lazy
    def macro(self):
        return self.template.macros['detail']

    @Lazy
    def resultSet(self):
        result = ResultSet([self.context])
        return result

    @Lazy
    def cells(self):
        return self.resultSet.rows.next().cells


class ListingView(BaseView):

    template = reportMacros

    @Lazy
    def macro(self):
        return self.template.macros['listing']

    @Lazy
    def resultSet(self):
        return ResultSet(self.context)

