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
SCORM interface definitions for API_1484_11.

$Id$
"""

from zope.interface import Interface, Attribute
from zope import schema


class IScormAPI(Interface):
    """ This interface represents a server-side adapter object for a
        tracking storage and a set of key/meta data that identify a
        learner session with one or more track objects. IScormAPI objects
        are stateless, so they don't remember any values between calls.

        In addition to the standard SCORM RTS methods there is a setValues()
        method that allows setting more than one value in one call,
        probably during execution of a Commit() call on the client
        side.

        There is no method corresponding to GetLastError() as the
        methods immediately return an appropriate CMIErrorCode,
        i.e. a '0' when OK.

        Note that the names of the methods have been slightly modified
        to correspond to the Python programming style guides.
    """

    taskId = Attribute('Task ID')
    runId = Attribute('Run ID (integer)')
    userId = Attribute('User ID')

    def init(taskId, runId, userId):
        """ Set the basic attributes with one call.
        """

    def initialize(parameter):
        """ Corresponds to API.Initialize('').
            Return CMIErrorCode.
        """

    def commit(parameter):
        """ Corresponds to API.Commit('').
            Return CMIErrorCode.
        """

    def terminate(parameter):
        """ Corresponds to API.Initialize('').
            Mark the run as finished.
            Return CMIErrorCode.
        """

    def setValue(element, value):
        """ Corresponds to API.SetValue(element, value).
            Return CMIErrorCode.
        """

    def setValues(mapping={}, **kw):
        """ Combine the mapping and kw arguments setting up a series of
            element-value mappings that will in turn be applied to a
            series of setValue() calls.
            Return CMIErrorCode.
        """

    def getValue(element):
        """ Corresponds to API.GetValue(element).
            Return a tuple with the current value of the element given
            (a string, '' if not present) and a CMIErrorCode.
        """

    def getErrorString(errorCode):
        """ Corresponds to API.GetErrorString(errorCode).
            Return the error text belonging to the errorCode
            (a CMIErrorCode value) given.
        """

    def getDiagnostic(code):
        """ Corresponds to API.GetDiagnostic(code).
            Return an LMS-specific information text related to the code given;
            code may but need not be a CMIErrorCode value.
        """
