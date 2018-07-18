import sys
import types

from .custom_property import list_property
from .custom_namedlist import NamedList, namedlist


class ListPropertyModule(types.ModuleType):
    """Custom callable module.

    This can be called by the following example.

    Example:

        ..code-block :: python

            >>> import list_property
            >>>
            >>> class Person(list):
            >>>    first_name = list_property(0, 'Hello')
            >>>    last_name = list_property(1, 'World!')
            >>>    middle_initial = list_property(2)  # Raises ValueError if li.other is called when index 2 is not set!
            >>>
            >>>    # Decorator automatically makes a setter function and replaces the default getter function.
            >>>    @list_property(3)
            >>>    def full_name(self):
            >>>        '''If not set use the first_name and the last_name.'''
            >>>        try:
            >>>            return self[3]
            >>>        except IndexError:
            >>>            return ''.join((self.first_name, self.last_name))
            >>>
            >>>    @middle_name.setter  # Replace the setter like a normal property
            >>>    def middle_name(self, value):
            >>>        self[2] = str(value)[0].upper()  # Use one letter as the middle initial


    This class module is implemented so you don't have to call
    ..code-block :: python

        >>> import list_property
        >>> list_property.list_property

    """
    list_property = staticmethod(list_property)
    NamedList = NamedList
    namedlist = staticmethod(namedlist)

    def __call__(self, index=None, default=ValueError("Invalid list_property value"),
                 fget=None, fset=None, fdel=None, doc=None):
        return self.list_property(index=index, default=default, fget=fget, fset=fset, fdel=fdel, doc=doc)


# Make this module callable
sys.modules[__name__] = ListPropertyModule(__name__)
