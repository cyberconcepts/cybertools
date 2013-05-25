#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
Utility functions.
"""

from zope.schema import vocabulary


class KeywordVocabulary(vocabulary.SimpleVocabulary):

    def __init__(self, items, *interfaces):
        """ ``items`` may be a tuple of (token, title) or a dictionary
            with corresponding elements named 'token' and 'title'.
        """
        terms = []
        for t in items:
            if type(t) is dict:
                token, title = t['token'], t['title']
            else:
                token, title = t
            terms.append(vocabulary.SimpleTerm(token, token, title))
        super(KeywordVocabulary, self).__init__(terms, *interfaces)

