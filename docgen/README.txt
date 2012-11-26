================================================================
docgen - Document Generation from Result Sets and XML Structures
================================================================

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest

  >>> from cybertools.docgen.base import WordDocument
  >>> doc = WordDocument(None, TestRequest)


Working with MHT Files
======================

  >>> import os
  >>> basePath = os.path.join(os.path.dirname(__file__), 'testing')

  >>> path = os.path.join(basePath, 'test_doc.mht')
  >>> f = open(path, 'rt')
  >>> data = f.read()
  >>> f.close()

  >>> imagePath = os.path.join(basePath, 'test_image.jpg')

  >>> from cybertools.docgen.mht import MHTFile
  >>> document = MHTFile(data)
  >>> document.addImage(imagePath)

  >>> body = '''
  ... '''

  >>> document.setBody(body)

  >>> outPath = os.path.join(basePath, 'out_doc.mht')
  >>> f = open(outPath, 'wt')
  >>> f.write(document.data)
  >>> f.close()

  >>> os.unlink(outPath)

