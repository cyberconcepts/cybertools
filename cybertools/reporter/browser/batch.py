# cybertools.reporter.browser.batch

""" A browser view class for batching to be used by a macro or some other
HTML providing template.
"""

import urllib.parse
from zope.cachedescriptors.property import Lazy
from cybertools.reporter.batch import Batch


class BatchView(object):

    default_size = 20

    def __init__(self, context, request, iterable=None):
        self.context = context
        self.request = request
        if iterable is not None:
            self.setup(iterable)

    def setup(self, iterable):
        form = self.request.form
        page = int(form.get('b_page', 1))
        size = int(form.get('b_size', self.default_size))
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
        params = {'b_page': page + 1, 'b_size': batch.size,
                  'b_overlap': batch.overlap, 'b_orphan': batch.orphan}
        form = self.request.form
        for p in form:
            if p not in params:
                break # we get UnicodeEncode errors here :-(
                v = form.get(p)
                if v:
                    params[p] = v
        return '?' + urllib.parse.urlencode(params)

    def url(self, page):
        return str(self.request.URL) + self.urlParams(page)

    def ajaxUrl(self, page):
        try:
            url = self.request.URL[-1]
        except KeyError: # make DocTest/TestRequest happy
            url = 'self.request.URL'
        return ''.join((url, '/@@ajax.inner.html', self.urlParams(page)))

    def navOnClick(self, page):
        return ("dojo.io.updateNode('body.contents', '%s'); "
                "return false;" % self.ajaxUrl(page))

    def info(self, page):
        return {'title': page+1,
                'url': self.url(page),
                'navOnClick': self.navOnClick(page)}

    def showNavigation(self):
        return self.first['title'] != self.last['title']


