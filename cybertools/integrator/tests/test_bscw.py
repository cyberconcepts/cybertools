
import os
import unittest, doctest
from zope.interface.verify import verifyClass


baseDir = os.path.dirname(os.path.dirname(__file__))
testDir = os.path.join(baseDir, 'testing', 'data')

flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def test_suite():
    return unittest.TestSuite((
                doctest.DocFileSuite('../bscw.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
