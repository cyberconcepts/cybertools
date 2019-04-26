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

  >>> xbody = '''<div class="WordSection1">
  ... <v:shape id="Grafik_x0020_2" o:spid="_x0000_i1025" type="#_x0000_t75"
  ...     style="width:320pt;height:240pt;visibility:visible;mso-wrap-style:square">
  ...   <v:imagedata src="FB-Besprechungsprotokoll-Dateien/image002.jpg" o:title=""/>
  ... </v:shape>
  ... </div>
  ... '''

  >>> body = '''<div class="WordSection1">
  ... <img src="files/test_image.jpg" />
  ... </div>
  ... '''

  >>> from cybertools.docgen.mht import MHTFile
  >>> document = MHTFile(data, body)

  >>> imageRefs = document.htmlDoc.getImageRefs()
  >>> for path in imageRefs:
  ...     imagePath = os.path.join(basePath, os.path.basename(path))
  ...     f = open(imagePath, 'rt')
  ...     imageData = f.read()
  ...     f.close()
  ...     document.addImage(imageData, path)

  >>> document.insertBody()

  >>> output = document.asString()
  >>> len(data), len(output)
  (294996, 336142)

  >>> outPath = os.path.join(basePath, 'out_doc.mht')
  >>> #f = open(outPath, 'wt')
  >>> #f.write(document.asString())
  >>> #f.close()

  >>> #os.unlink(outPath)

