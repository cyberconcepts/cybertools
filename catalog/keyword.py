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

"""Keyword catalog index.

$Id$
"""

import zope.index.keyword
import zope.interface

import zope.app.container.contained
import zope.app.catalog.attribute
import zope.app.catalog.interfaces


class IKeywordIndex(zope.app.catalog.interfaces.IAttributeIndex,
                    zope.app.catalog.interfaces.ICatalogIndex):
    """Interface-based catalog keyword index.
    """


class KeywordIndex(zope.app.catalog.attribute.AttributeIndex,
                 zope.index.keyword.KeywordIndex,
                 zope.app.container.contained.Contained):

    zope.interface.implements(IKeywordIndex)

