#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Action handler for sending emails.

$Id$
"""

from email.MIMEText import MIMEText
from zope import component
from zope.interface import implements

from cybertools.composer.interfaces import IInstance
from cybertools.composer.rule.base import ActionHandler


class MailActionHandler(ActionHandler):

    def __call__(self, data, params={}):
        sender = params.get('sender', 'unknown')
        client = self.context.context
        clientData = IInstance(client).applyTemplate()
        recipient = clientData['standard.email']
        msg = self.prepareMessage(data.subjectLine, data.text, sender, recipient)
        data['mailInfo'] = self.sendMail(msg.as_string(), sender, [recipient])
        return data

    def prepareMessage(self, subject, text, sender, recipient):
        text = text.encode('utf-8')
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
