# cybertools.pyscript.browser

"""Python Script Browser Views
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
        if isinstance(result, str):
            return result
        return result.decode()


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
