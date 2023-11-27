======================
Media Asset Management
======================

  ($Id$)

  >>> import os
  >>> from cybertools.media.tests import dataDir, clearDataDir
  >>> from cybertools.media.asset import MediaAssetFile

  >>> image1 = os.path.join(dataDir, 'test1.jpg')


Image Transformations
=====================

  >>> rules = dict(
  ...           minithumb='size(96, 1000)',
  ... )

  >>> asset = MediaAssetFile(image1, rules, 'image/jpeg')

  >>> asset.getImageSize()
  (238, 191)
  >>> asset.getImageSize('minithumb')
  (96, 77)

  >>> asset.transform()


Fin de Partie
=============

  >>> clearDataDir()
