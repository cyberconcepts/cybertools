
import unittest, doctest


def test_suite():
    return unittest.TestSuite((
                doctest.DocFileSuite('README.txt'),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
