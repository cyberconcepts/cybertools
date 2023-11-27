#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
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
Advanced properties, i.e. the lazy one and Philipp von Weitershausen's
read & write properties.

Based on zope.cachedescriptors.property.Lazy and including code from
http://cheeseshop.python.org/pypi/rwproperty.

$Id$
"""

class lzprop(object):
    """Declare lazy properties that are calculated only if needed,
       and just once.

       See property.txt for example usage.
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, inst, class_):
        if inst is None: return self
        value = self.func(inst)
        inst.__dict__[self.func.__name__] = value
        return value


# Read & write properties
#
# Copyright (c) 2006 by Philipp "philiKON" von Weitershausen
#                       philikon@philikon.de
#
# Freely distributable under the terms of the Zope Public License, v2.1.
#
# See rwproperty.txt for detailed explanations
#
import sys

__all__ = ['getproperty', 'setproperty', 'delproperty']

class rwproperty(object):

    def __new__(cls, func):
        name = func.__name__

        # ugly, but common hack
        frame = sys._getframe(1)
        locals = frame.f_locals

        if name not in locals:
            return cls.createProperty(func)

        oldprop = locals[name]
        if isinstance(oldprop, property):
            return cls.enhanceProperty(oldprop, func)

        raise TypeError("read & write properties cannot be mixed with "
                        "other attributes except regular property objects.")

    # this might not be particularly elegant, but it's easy on the eyes

    @staticmethod
    def createProperty(func):
        raise NotImplementedError

    @staticmethod
    def enhanceProperty(oldprop, func):
        raise NotImplementedError

class getproperty(rwproperty):

    @staticmethod
    def createProperty(func):
        return property(func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(func, oldprop.fset, oldprop.fdel)

class setproperty(rwproperty):

    @staticmethod
    def createProperty(func):
        return property(None, func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(oldprop.fget, func, oldprop.fdel)

class delproperty(rwproperty):

    @staticmethod
    def createProperty(func):
        return property(None, None, func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(oldprop.fget, oldprop.fset, func)
