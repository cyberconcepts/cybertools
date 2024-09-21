# cybertools.composer.schema.factory

""" Schema factory stuff.
"""

from zope.component import adapts
from zope.interface import implementer
from zope.interface import Interface
from zope import schema

from cybertools.composer.schema.field import Field
from cybertools.composer.schema.interfaces import ISchemaFactory, ISchemaProcessor
from cybertools.composer.schema.schema import Schema


class Email(schema.TextLine):

    __typeInfo__ = ('email',)


# put field type name and other info in standard field classes.
schema.Field.__typeInfo__ = ('textline',)
schema.Password.__typeInfo__ = ('password',)
schema.Int.__typeInfo__ = ('number',)
schema.Float.__typeInfo__ = ('decimal',)
schema.Choice.__typeInfo__ = ('dropdown',)


@implementer(ISchemaFactory)
class SchemaFactory(object):
    """ Creates a cybertools.composer schema from an
        interface (a zope.schema schema).
    """

    adapts(Interface)

    fieldMapping = {
            #schema.TextLine: ('textline',),
            #schema.ASCIILine: ('textline',),
            #schema.Password: ('password',),
            schema.Text: ('textarea',),
            schema.ASCII: ('textarea',),
            schema.Date: ('date',),
            schema.Datetime: ('date',),
            #schema.Int: ('number',),
            #schema.Float: ('decimal',),
            schema.Bool: ('checkbox',),
            schema.List: ('list',),
            #schema.Choice: ('dropdown',),
            schema.Bytes: ('fileupload',),
            #Email: ('email',),
    }

    def __init__(self, context):
        self.context = context
        self.schemaProcessor = ISchemaProcessor(self, None)

    def __call__(self, interface, **kw):
        fieldMapping = self.fieldMapping
        fields = []
        omit = kw.pop('omit', [])
        include = kw.pop('include', [])
        for fname in schema.getFieldNamesInOrder(interface):
            if fname in omit:
                continue
            if include and fname not in include:
                continue
            field = interface[fname]
            if getattr(field, 'suppress', False):
                continue
            #if getattr(field, 'hidden', False):
            #    continue
            info = fieldMapping.get(field.__class__)
            f = createField(field, info)
            if self.schemaProcessor is not None:
                f = self.schemaProcessor.process(f, **kw)
            if f is not None:
                fields.append(f)
        return Schema(name=interface.__name__, *fields, **kw)


def createField(field, info=None):
    if info is None:
        info = getattr(field, '__typeInfo__', ('textline',))
    voc = (getattr(field, 'vocabulary', ()) or
           getattr(field, 'vocabularyName', None))
    f = Field(field.getName(),
              fieldType=info[0],
              fieldTypeInfo=len(info) > 1 and info[1] or None,
              required=field.required,
              default=field.default,
              default_method=getattr(field, 'default_method', None),
              vocabulary=voc,
              title=field.title,
              description=field.description,
              readonly=field.readonly,
              #value_type=getattr(field, 'value_type', None),
              nostore=getattr(field, 'nostore', False),
              showEmpty=getattr(field, 'showEmpty', False),
              multiple=getattr(field, 'multiple', False),
              display_format=getattr(field, 'displayFormat', None),
              baseField=field,)
    return f
