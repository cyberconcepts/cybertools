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
Generate strange (not guessable) UIDs.

$Id$
"""

import random


bits = 128


def generateUid(check=None, lowerCaseOnly=False, bits=bits, seed=None, base=62):
    """ Generates a unique ID.
    """
    random.seed(seed)
    OK = False
    base = lowerCaseOnly and min(base, 36) or base
    while not OK:
        data = strBase(random.getrandbits(bits), base)
        OK = check is None or check(data)
    return data


def strBase(n, base):
    result = []
    while n > 0:
        n, r = divmod(n, base)
        result.append(r)
    return ''.join(reversed([toChar(n) for n in (result or [0])]))

def toChar(n):
    return n < 10 and chr(48+n) or n < 36 and chr(87+n) or chr(29+n)

