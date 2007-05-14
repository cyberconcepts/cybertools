================================================================
Composer - Building Complex Structures with Templates or Schemas
================================================================

  ($Id$)

  >>> from cybertools.composer.base import Element, Compound, Template
  >>> from cybertools.composer.client import Instance, Client

We set up a very simple demonstration system using a PC configurator.
We start with two classes denoting a configuration and a simple
component within this configuration.

  >>> class Configuration(Template):
  ...     def __init__(self, name):
  ...         self.name = name
  ...         super(Configuration, self).__init__()

  >>> class BasicComponent(Element):
  ...     def __init__(self, name):
  ...         self.name = name
  ...     def __repr__(self):
  ...         return self.name

  >>> desktop = Configuration('Desktop')
  >>> desktop.components.append(BasicComponent('case'))
  >>> desktop.components.append(BasicComponent('mainboard'))
  >>> desktop.components.append(BasicComponent('cpu'))
  >>> desktop.components.append(BasicComponent('harddisk'))

Now somebody wants to configure a desktop PC using this configuration.
We need another class denoting the product that will be created.

  >>> class Product(object):
  ...     def __init__(self, productId):
  ...         self.productId = productId
  ...         self.parts = {}
  ...     def __repr__(self):
  ...         return self.productId

  >>> c001 = Product('c001')

The real stuff will be done by an instance that connects the product
(via the client) with the template.

  >>> class ConfigurationInstance(Instance):
  ...     def applyTemplate(self):
  ...         for c in self.template.components:
  ...             print c, self.parent.context.parts.get(c.name, '-')

In this case we can directly use the basic client adapter for setting up the
connection. As we have only one template we also associate only one
instance with the client.

  >>> client = Client(c001)
  >>> client.instances.append(ConfigurationInstance(client, desktop))
  >>> client.applyTemplates()
  case -
  mainboard -
  cpu -
  harddisk -

If we have configured a CPU for our configuration this will be listed.

  >>> c001.parts['cpu'] = Product('z80')
  >>> client.applyTemplates()
  case -
  mainboard -
  cpu z80
  harddisk -

Note that the ConfigurationInstance's applyTemplate() method is fairly
primitive. In a real-world application there usually are a lot more methods
that do more stuff. In our PC configurator application there might be
methods that just list components (e.g. to provide a user interface),
retrieve candidate products (e.g. CPUs) to use in the
configuration and store the user's selection in the context object.

