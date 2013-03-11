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
Date and time utilities.
"""

import time
from datetime import datetime
try:
    import pytz
except ImportError:
    pytz = None


def getTimeStamp():
    return int(time.time())

def date2TimeStamp(d):
    return int(time.mktime(d.timetuple()))


def timeStamp2Date(ts, useGM=False):
    if ts is None:
        ts = getTimeStamp()
    return datetime.fromtimestamp(ts)

def timeStamp2ISO(ts, useGM=False, format='%Y-%m-%d %H:%M'):
    return formatTimeStamp(ts, useGM, format)

def formatTimeStamp(ts, useGM=False, format='%Y-%m-%d %H:%M'):
    if ts is None:
        ts = getTimeStamp()
    fct = useGM and time.gmtime or time.localtime
    return time.strftime(format, fct(ts))


def str2timeStamp(s):
    try:
        t = time.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            t = time.strptime(s, '%Y-%m-%d %H:%M')
        except ValueError:
            t = time.strptime(s, '%Y-%m-%d')
    return int(time.mktime(t))


def strptime(s, format='%Y-%m-%d %H:%M:%S'):
    return datetime(*(time.strptime(s, format)[:6]))


def year(d=None):
    if d is None:
        d = datetime.today()
    return d.year


def toLocalTime(d):
    if pytz is None:
        return d
    cet = pytz.timezone('CET')
    return d.astimezone(cet)
