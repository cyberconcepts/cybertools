==================================
Dynamically Loaded Plug-in Modules
==================================

  ($Id$)

  >>> import os
  >>> basePath = os.path.join(os.path.dirname(__file__), 'testing')


Create, Modify, and Reload Plug-in Modules
==========================================

Let's first create a module with a function we'll call later.

  >>> mod1Path = os.path.join(basePath, 'mod1.py')
  >>> src = '''
  ... from cybertools.plugin.base import register
  ...
  ... @register()
  ... def show():
  ...     print 'mod1.show() executed'
  ... '''
  >>> f = open(mod1Path, 'w')
  >>> f.write(src)
  >>> f.close()

We could import this module now immediately but in order to be able to
automatically reload it later (and to be able to look it up in the plug-in
module registry) we include it in a loader module.

  >>> loadPath = os.path.join(basePath, 'load.py')
  >>> src = '''
  ... from cybertools.plugin.manage import loadModules
  ...
  ... from cybertools.plugin.testing import mod1
  ... loadModules(mod1)
  ...
  ... '''
  >>> f = open(loadPath, 'w')
  >>> f.write(src)
  >>> f.close()

Now we first import the load module, then import the test module and call
the function in it.

  >>> from cybertools.plugin.testing import load

  >>> from cybertools.plugin.testing import mod1
  >>> mod1.show()
  mod1.show() executed

We now append additional code to mod1 and see if it is reloaded automatically.

  >>> src = '''    print 'now changed...'
  ...
  ... '''
  >>> f = open(mod1Path, 'a')
  >>> f.write(src)
  >>> f.close()

(In order to create a sufficient time difference during testing we patch the
stored setting. We also have to remove the .pyc file, otherwise Python will
refuse to recompile the source file because the modification time is not changed
significantly during the run of the test script.)

  >>> from cybertools.plugin.manage import modules
  >>> modules['cybertools.plugin.testing.mod1'].timeStamp -= 2
  >>> os.remove(os.path.join(basePath, 'mod1.pyc'))

  >>> mod1.show()
  mod1.show() executed
  now changed...

Let's append another function to the source file.

  >>> src = '''
  ... @register()
  ... def another():
  ...     print 'executing another function.'
  ...
  ... '''
  >>> f = open(mod1Path, 'a')
  >>> f.write(src)
  >>> f.close()

  >>> modules['cybertools.plugin.testing.mod1'].timeStamp -= 2
  >>> os.remove(os.path.join(basePath, 'mod1.pyc'))

When we try to call the new function, the module will not be reloaded
automatically.

  >>> mod1.another()
  Traceback (most recent call last):
  ...
  AttributeError: 'module' object has no attribute 'another'

But just reloading the load module will also update the mod1 application module.

  >>> reload(load)
  <module 'cybertools.plugin.testing.load' ...>
  >>> mod1.another()
  executing another function.


Fin de partie
=============

  >>> for fn in ('mod1', 'load'):
  ...     os.remove(os.path.join(basePath, fn) + '.py')
  ...     os.remove(os.path.join(basePath, fn) + '.pyc')
