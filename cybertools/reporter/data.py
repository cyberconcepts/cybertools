# cybertools.reporter.data

""" Basic data / data source implementations.
"""

from zope.interface import implementer
from cybertools.reporter.interfaces import IDataSource


@implementer(IDataSource)
class DataSource(object):

    def __init__(self, iterable):
        self.data = iterable

    def __iter__(self):
        return iter(self.data)
