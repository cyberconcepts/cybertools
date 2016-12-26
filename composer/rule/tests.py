
import unittest, doctest
from email import message_from_string
from zope.interface import implements
from zope.sendmail.interfaces import IMailDelivery


class TestMailer(object):

    implements(IMailDelivery)

    def send(self, sender, recipients, message):
        print 'sender:', sender
        print 'recipients:', recipients
        msg = message_from_string(message)
        print 'subject:', msg['Subject']
        print 'message:'
        print msg.get_payload(decode=True)


class Test(unittest.TestCase):
    "Basic tests."

    def testBasics(self):
        pass


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    return unittest.TestSuite((
                unittest.makeSuite(Test),
                doctest.DocFileSuite('README.txt', optionflags=flags),
            ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
