# cybertools.pyscript.plog

""" Management of filesystem images (plots) and corresponding views.
"""

import os
import time
from zope.cachedescriptors.property import Lazy

from cybertools.util import randomname, jeep


class CachedImage(object):
    """ Keep information about temporary image files.
    """

    def __init__(self, path, name=None):
        self.path = path
        if name is None:
            self.name = randomname.generateName(lambda x: x not in cachedImages.keys())
        else:
            self.name = name
        self.timeStamp = int(time.time())


cachedImages = jeep.Jeep()

def registerImage(filename, name=None):
    image = CachedImage(filename, name)
    cachedImages.append(image)
    while len(cachedImages) > 10:  # clean up old cache entries
        old = cachedImages.pop(0).path
        if os.path.exists(old):
            os.unlink(old)
    return image.name


class PlotView(object):
    """ Access to temporary filesystem images.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def __call__(self):
        if self.traverse_subpath:
            key = self.traverse_subpath[0]
        else:
            key = self.request.form.get('image', 'not_found')
        if '.' in key:  # remove extension possibly added to make Flash happy
            key = key.split('.', 1)[0]
        path = cachedImages[key].path
        self.setHeaders(path)
        f = open(path, 'rb')
        data = f.read()
        f.close()
        return data

    def setHeaders(self, name=None):
        response = self.request.response
        # TODO: get content type from name (extension)
        response.setHeader('Content-Type', 'image/jpeg')
        response.setHeader('Expires', 'Sat, 1 Jan 2000 00:00:00 GMT');
        response.setHeader('Pragma', 'no-cache');

