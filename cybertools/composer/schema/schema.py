# cybertools.composer.schema.schema

""" Basic classes for schemas, i.e. sets of fields that may be used for creating
editing forms or display views for objects.
"""

from zope.interface import implementer

from cybertools.composer.base import Component, Element, Compound
from cybertools.composer.base import Template
from cybertools.composer.schema.interfaces import ISchema, IFormState
from cybertools.util.jeep import Jeep


@implementer(ISchema)
class Schema(Template):

    name = u''
    labelWidth = 'auto'
    manager = None

    def __init__(self, *fields, **kw):
        name = kw.get('name', None)
        if name is not None:
            self.name = name
        manager = kw.get('manager', None)
        if manager is not None:
            self.manager = self.__parent__ = manager
        super(Schema, self).__init__()
        for f in fields:
            self.components.append(f)

    @property
    def fields(self):
        return self.getFields()

    def getFields(self):
        return self.components

    @property
    def __name__(self):
        return self.name

    def getManager(self):
        return self.manager


@implementer(IFormState)
class FormState(object):

    def __init__(self, fieldInstances=None, changed=False, severity=0):
        if fieldInstances is None:
            fieldInstances = []
        self.fieldInstances = Jeep(fieldInstances)
        self.changed = changed
        self.severity = severity


class FormError(object):

    def __init__(self, title, description=None, severity=5):
        self.title = title
        self.description = description or title
        self.severity = severity

    def __str__(self):
        return self.title

    def __repr__(self):
        return "FormError('%s')" % self.title


formErrors = dict(
    required_missing=FormError(u'Missing data for required field',
        u'Please enter data for required field.'),
    invalid_number=FormError(u'Invalid number',
        u'Please enter a number, only digits allowed.'),
    invalid_datetime=FormError(u'Invalid date/time',
        u'Please enter a string denoting a valid date/time.'),
    invalid_email_address=FormError(u'Invalid E-Mail Address',
        u'Please enter a valid email address.'),
)
