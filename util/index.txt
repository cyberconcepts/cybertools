========================================
Indexed Collections for Various Purposes
========================================

$Id$

Multikey Dictionaries
=====================

A MultiKeyDict is a dictionary that expects its keys to be tuples.

  >>> from cybertools.index.multikey import MultiKeyDict
  >>> registry = MultiKeyDict()

  >>> registry[('index.html', None, None, None)] = 'global index.html'

  >>> registry[('index.html', None, None, None)]
  'global index.html'

So this would be nothing special - any dictionary is able to provide this
functionality; but a MultiKeyDict has some fallback mechanisms for retrieving
objects only partly fitting the requested key:

  >>> registry[('index.html', 'topic', 'zope3', 'Custom')]
  'global index.html'

  >>> registry[('index.html', 'topic', None, None)] = 'index.html for type "topic"'

  >>> registry[('index.html', 'topic', 'zope3', 'Custom')]
  'index.html for type "topic"'

It is also possible to keep intermediate parts of a key variable by
setting them to None:

  >>> registry[('index.html', None, None, 'Custom')] = 'Global index.html for Custom skin'

The more on the left a matching key part is the higher is its priority:

  >>> registry[('index.html', 'topic', 'zope3', 'Custom')]
  'index.html for type "topic"'

  >>> registry[('index.html', 'task', 'bugfixes', 'Custom')]
  'Global index.html for Custom skin'

Index entries that are present in the stored dictionary must always match:

  >>> registry[('edit.html', 'topic', 'zope3', 'Custom')] = 'very special edit.html'

  >>> registry[('index.html', 'task', 'bugfixes', 'Custom')]
  'Global index.html for Custom skin'

  >>> registry[('index.html', 'topic', 'zope3', 'Custom')]
  'index.html for type "topic"'

  >>> registry.get(('edit.html', 'task', 'bugfixes', 'Custom')) is None
  True

  >>> registry[('edit.html', None, None, 'Custom')] = 'edit.html for Custom skin'

  >>> registry.get(('edit.html', 'task', 'bugfixes', '')) is None
  True

  >>> registry[('edit.html', 'task', 'bugfixes', 'Custom')]
  'edit.html for Custom skin'

If you don't know any more what entries we had added to the registry just
query its items() method:

  >>> registry.items()
  ((('edit.html', 'topic', 'zope3', 'Custom'), 'very special edit.html'),
   (('edit.html', None, None, 'Custom'), 'edit.html for Custom skin'),
   (('index.html', None, None, None), 'global index.html'),
   (('index.html', None, None, 'Custom'), 'Global index.html for Custom skin'),
   (('index.html', 'topic', None, None), 'index.html for type "topic"'))
