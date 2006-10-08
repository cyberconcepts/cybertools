===============================
Controlling the storage of data
===============================

  ($Id$)

  >>> import os
  >>> from cybertools import storage
  >>> directory = os.path.dirname(storage.__file__)

  >>> from cybertools.storage.filesystem import explicitDirectoryStorage
  >>> storage = explicitDirectoryStorage(os.path.join(directory, 'testdata'))
  >>> storage.getDir('demo')
  '/home/.../cybertools/storage/testdata/demo'


