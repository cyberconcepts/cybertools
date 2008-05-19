#
#  Copyright (c) 2008 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Fake BSCW repository for testing purposes.

$Id$
"""

from xmlrpclib import Fault

from cybertools.integrator import bscw


class Artifact(dict):

    attributes = bscw.baseAttributes
    repository = None

    def __init__(self, id, **kw):
        if not id.startswith('bs_'):
            id = 'bs_' + id
        self.id = self['id'] = self['__id__'] = id
        self.children = kw.pop('children', [])
        self['__class__'] = kw.pop('__class__', 'cl_core.Folder')
        self.update(kw)

    def getData(self, attrs):
        return dict((key, self[key]) for key in attrs if key in self)


class BSCWRepository(dict):

    def __init__(self, *objs):
        for obj in objs:
            self[obj.id] = obj
            obj.repository = self
        self.updateContainersAttribute()

    def get(self, key, default=None):
        if not key.startswith('bs_'):
            key = 'bs_' + key
        return super(BSCWRepository, self).get(key, default)

    def updateContainersAttribute(self):
        for obj in self.values():
            for c in obj.children:
                child = self.get(c)
                if child is not None:
                    containerInfo = dict(__id__=child.id, name=child['name'])
                    child.setdefault('containers', []).append(containerInfo)


sampleObjects = BSCWRepository(
    Artifact('4', name='public', descr='Public Repository', children=['5'],
                  containers=[dict(__id__='4711', name='Community of Anonymous')]),
    Artifact('5', name='Introduction', descr='Introduction to BSCW'),
)


class BSCWServer(object):

    def __init__(self, objects):
        self. objects = objects

    def get_attributes(self, id=None, attribute_names=['__id__', 'name'], depth=0,
                       nested=False, offset=0, number=0, sorted_by=None):
        obj = self.objects.get(id)
        if obj is None:
            raise Fault(10101, 'Bad object id: %s' % id)
        result = [obj.getData(attribute_names)]
        if nested:
            for level in range(depth):
                for id in obj.children:
                    result.append(self.get_attributes(id, attribute_names,
                                  depth-1, nested, offset, number, sorted_by))
        return result

    def get_attributenames(self, __class__):
        return baseAttributes

    def get_document(self, id, version_id):
        obj = self.objects.get(id)
        if obj is None:
            raise Fault(10101, 'Bad object id: %s' % id)
        return ''

    def get_path(id):
        return self.get_attributes(id, ['containers'])[0].get('containers', [])

