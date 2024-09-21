# cybertools.browser.form

"""Form Controller stuff: form processing is the part of the
model/view/controller pattern that deals withform input.
"""

from zope.interface import Interface, implementer


class IFormController(Interface):
    """ Used as a named adapter by GenericView for processing form input.
    """

    def update():
        """ Processing form input...
        """


@implementer(IFormController)
class FormController(object):

    def __init__(self, context, request):
        self.view = self.__parent__ = view = context
        self.context = view.context # the controller is adapted to a view
        self.request = request

    def update(self):
        pass

