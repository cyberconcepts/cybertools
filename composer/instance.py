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
Base classes to be used for client adapters.

$Id$
"""

from zope.interface import implements

from cybertools.composer.interfaces import IInstance


class Instance(object):

    implements(IInstance)

    templateStorage = dict
    templateAttributeName = '__ctc_templates__'

    aspect = 'composer.default'

    def __init__(self, context):
        self.context = context
        self.instances = []

    def setTemplate(self, template):
        templates = getattr(self.context,
                            self.templateAttributeName, self.templateStorage())
        templates.setdefault(self.aspect, template)
        setattr(self.context, self.templateAttributeName, templates)
    def getTemplate(self):
        templates = getattr(self.context, self.templateAttributeName, {})
        return templates.get(self.aspect, None)
    template = property(getTemplate, setTemplate)

    def applyTemplate(self, *args, **kw):
        raise ValueError('To be implemented by subclass')

