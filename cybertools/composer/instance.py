# cybertools.composer.instance

""" Base classes to be used for client adapters.
"""

from zope.interface import implementer

from cybertools.composer.interfaces import IInstance


@implementer(IInstance)
class Instance(object):

    templateFactory = dict
    templateAttributeName = '__ctc_template__'

    aspect = 'composer.default'

    def __init__(self, context):
        self.context = context

    def setTemplate(self, temp):
        template = getattr(self.context,
                           self.templateAttributeName,
                           self.templateFactory())
        template.setdefault(self.aspect, temp)
        setattr(self.context, self.templateAttributeName, template)
    def getTemplate(self):
        template = getattr(self.context, self.templateAttributeName, {})
        return template.get(self.aspect, [])
    template = property(getTemplate, setTemplate)

    def applyTemplates(self, *args, **kw):
        raise ValueError('To be implemented by subclass')

