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
Some simple standard formatting routines.

$Id$
"""

from zope.i18n.locales import locales
from datetime import datetime


def nl2br(text):
    if not text: return text
    if '\n' in text: # Unix or DOS line endings
        return '<br />\n'.join(x.replace('\r', '') for x in text.split('\n'))
    else: # gracefully handle Mac line endigns
        return '<br />\n'.join(text.split('\r'))


def formatDate(dt=None, type='date', variant='medium', lang='de'):
    """ type: date, time, dateTime;
        variant: full, long, medium, short.
    """
    loc = locales.getLocale(lang)
    fmt = loc.dates.getFormatter(type, variant)
    return fmt.format(dt or datetime.now())


def formatNumber(num, type='decimal', lang='de'):
    loc = locales.getLocale(lang)
    fmt = de.numbers.getFormatter(type)
    return fmt.format(num)

