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

from zope.cachedescriptors.property import Lazy
from cybertools.reporter.batch import Batch


class BatchView(object):

    def __init__(self, context, request, iterable=None):
        self.context = context
        self.request = request
        if iterable is not None:
            self.setup(iterable)

    def setup(self, iterable):
        form = self.request.form
        page = int(form.get('b_page', 1))
        size = int(form.get('b_size', 20))
        overlap = int(form.get('b_overlap', 0))
        orphan = int(form.get('b_orphan', 0))
        self.batch = Batch(iterable, page-1, size, overlap, orphan)
        return self

    def items(self):
        return self.batch.items

    @Lazy
    def current(self):
        return self.info(self.batch.getIndexRelative(0))

    @Lazy
    def first(self):
        return self.info(self.batch.getIndexAbsolute(0))

    @Lazy
    def last(self):
        return self.info(self.batch.getIndexAbsolute(-1))

    @Lazy
    def previous(self):
        return self.info(self.batch.getIndexRelative(-1))

    @Lazy
    def next(self):
        return self.info(self.batch.getIndexRelative(1))

    def urlParams(self, page):
        batch = self.batch
        return ('?b_page=%i&b_size=%i&b_overlap=%i&b_orphan=%i'
                    % (page+1, batch.size, batch.overlap, batch.orphan) )

    def url(self, page):
        return str(self.request.URL) + self.urlParams(page)

    def info(self, page):
        return {'title': page+1, 'url': self.url(page)}

    def showNavigation(self):
        return self.first['title'] != self.last['title']


