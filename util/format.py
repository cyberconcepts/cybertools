#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
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
"""

from zope.i18n.locales import locales
from datetime import datetime


def nl2br(text):
    if not text:
        return text
    if '\n' in text: # Unix or DOS line endings
        return '<br />\n'.join(x.replace('\r', '') for x in text.split('\n'))
    else: # gracefully handle Mac line endigns
        return '<br />\n'.join(text.split('\r'))

def nl2pipe(text):
    if not text:
        return text
    if '\n' in text: # Unix or DOS line endings
        return ' | '.join(x.replace('\r', '') for x in text.split('\n'))
    else:
        return ' | '.join(text.split('\r'))


def formatDate(dt=None, type='date', variant='medium', lang='de'):
    """ type: date, time, dateTime;
        variant: full, long, medium, short.
    """
    loc = locales.getLocale(lang)
    fmt = loc.dates.getFormatter(type, variant)
    return fmt.format(dt or datetime.now())


def formatNumber(num, type='decimal', lang='de', pattern=u'#,##0.00;-#,##0.00'):
    loc = locales.getLocale(lang)
    fmt = loc.numbers.getFormatter(type)
    return fmt.format(num, pattern=pattern)



def toStr(value, encoding='UTF-8'):
    if isinstance(value, unicode):
        return value.encode(encoding)
    return str(value)

def toUnicode(value, encoding='UTF-8', fallback='ISO8859-15'):
    # or: fallback='CP852'
    if isinstance(value, unicode):
        return value
    elif isinstance(value, str):
        try:
            return value.decode(encoding)
        except UnicodeDecodeError:
            return value.decode(fallback)
    else:
        return u''
