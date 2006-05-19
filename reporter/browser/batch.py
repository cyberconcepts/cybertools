#
#  Copyright (c) 2006 Helmut Merz helmutm@cy55.de
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
A browser view class for batching to be used by a macro or some other
HTML providing template.

$Id$
"""

from cybertools.reporter.batch import Batch


class BatchView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        form = request.form
        page = int(form.get('b_page', 1))
        size = int(form.get('b_size', 20))
        overlap = int(form.get('b_overlap', 0))
        orphan = int(form.get('b_orphan', 0))
        self.batch = Batch(context, page-1, size, overlap, orphan)

    def items(self):
        return setupUrlParams(self.batch.items)

    def first(self):
        return setupUrlParams(self.batch.getIndexAbsolute(0))

    def last(self):
        return setupUrlParams(self.batch.getIndexAbsolute(-1))

    def previous(self):
        return setupUrlParams(self.batch.getIndexRelative(1))

    def next(self):
        return setupUrlParams(self.batch.getIndexRelative(-1))

    def setupUrlParams(self, page):
        return ('?b_page=%i&b_size=%i&b_overlap=%i&b_orphan=%i'
                    % (page, self.size, self.overlap, self.orphan) )

    
