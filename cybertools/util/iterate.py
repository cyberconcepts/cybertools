# cybertools.util.iterate

""" Iterator and generator utilities.
"""

from itertools import islice


class BatchIterator(object):

    def __init__(self, data, limit=20, start=0):
        self.data = iter(data)
        self.limit = limit
        self.start = start
        self.count = 0
        self.batch = 0
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= (self.batch + 1) * self.limit:
            raise StopIteration
        if self.start:
            for i in islice(self.data, 0, self.start*self.limit):
                pass
            self.start = 0
        self.count += 1
        try:
            return self.data.__next__()
        except StopIteration:
            self.exhausted = True
            raise

    def advance(self, batches=1):
        self.batch += batches
        return not self.exhausted
