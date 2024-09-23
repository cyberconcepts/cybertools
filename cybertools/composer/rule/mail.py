# cybertools.composer.rule.mail

""" Action handler for sending emails.
"""

from email.mime.text import MIMEText
from zope import component

from cybertools.composer.interfaces import IInstance
from cybertools.composer.rule.interfaces import IActionHandler
from cybertools.composer.rule.base import ActionHandler


class MailActionHandler(ActionHandler):

    def __call__(self, data, params={}):
        sender = params.get('sender', 'unknown')
        client = self.context.context
        clientData = IInstance(client).applyTemplate()
        recipient = clientData['standard.email']
        if 'messageName' in params:
            mh = component.getAdapter(self.context, IActionHandler, name='message')
            data = mh(data, params)
        msg = self.prepareMessage(data['subjectLine'], data['text'],
                                  sender, recipient)
        data['mailInfo'] = self.sendMail(msg.as_string(), sender, [recipient])
        return data

    def prepareMessage(self, subject, text, sender, recipient):
        #text = text.encode('utf-8')
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        return msg

    def sendMail(self, message, sender, recipients):
        from zope.sendmail.interfaces import IMailDelivery
        mailhost = component.getUtility(IMailDelivery, 'Mail')
        mailhost.send(sender, recipients, message)
        return 'Mail sent to %s.' % ', '.join(recipients)
