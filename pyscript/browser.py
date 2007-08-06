##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Python Script Browser Views

$Id$
"""

from zope.app.form.browser.editview import EditView
from zope.app.i18n import ZopeMessageFactory as _


class PythonScriptEval(object):
    """Evaluate the Python Script."""

    def index(self, **kw):
        """Call a Python Script"""
        self.request.response.setHeader('content-type',
                                        self.context.contentType)
        result = self.context(self.request, **kw)
        if type(result) is unicode:
            return result
        return unicode(result)


class PythonScriptEditView(EditView):
    """Edit View Class for Python Script."""

    syntaxError = None

    def update(self):
        """Update the content with the HTML form data."""
        try:
            status = super(PythonScriptEditView, self).update()
        except SyntaxError, err:
            self.syntaxError = err
            status = _('A syntax error occurred.')
            self.update_status = status

        return status