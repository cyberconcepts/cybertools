#
#  Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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
Pre-processor for supporting the MediaWiki link format.

$Id$
"""

import re


linkPattern = re.compile(r'\[\[(.+)\]\]')


def preprocess(source):
    result = linkPattern.sub(processLinkPattern, source)
    return result


def processLinkPattern(match):
    value = match.group(1)
    parts = value.split('|')
    name = parts.pop(0).strip()
    if ':' in name:
        prefix, name = name.split(':', 1)
        return createRstxImage(name, parts, prefix)
    else:
        return createRstxLink(name, parts)

def createRstxLink(name, parts, prefix=None):
    text = parts and parts[-1].strip() or name
    return '`%s <%s>`__' % (text, name)

def createRstxImage(name, parts, prefix=None):
    return '\n\n.. image:: %s\n\n' % name


