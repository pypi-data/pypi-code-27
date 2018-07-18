

__all__ = ['list_property']


class ListProperty(property):
    """Property that is really just a list index. This can turn a list into an object like a named tuple only a list
    is mutable.
    """
    def __init__(self, index=None, default=ValueError("Invalid list_property value"),
                 fget=None, fset=None, fdel=None, doc=None):
        """Property that is really just a list index

        Args:
            index (int): The list index position associated with this property
            default (object)[ValueError]: The default value or Exception when the index/value has not been set.
            fget (function)[None]: Getter function
            fset (function)[None]: Setter function
            fdel (function)[None]: Deleter function
            doc (str)[None]: Documentation

        Alt Args:
            fget (function)[None]: Getter function
            fset (function)[None]: Setter function
            fdel (function)[None]: Deleter function
            doc (str)[None]: Documentation
            index (int): The list index position associated with this property
            default (object)[ValueError]: The default value or Exception when the index/value has not been set.
        """
        # Swap arguments
        if not isinstance(index, int):
            fget, index = index, None
            if callable(default):
                fset, default = default, None

        self.index = index
        self.default = default

        if fget is None:
            fget = self.get_value
        if fset is None:
            fset = self.set_value

        super().__init__(fget, fset, fdel, doc)

    def getter(self, fget):
        return type(self)(self.index, self.default, fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.index, self.default, self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.index, self.default, self.fget, self.fset, fdel, self.__doc__)

    def __call__(self, fget):
        return self.getter(fget)

    def get_value(self, obj):
        try:
            return obj[self.index]
        except Exception as err:
            if isinstance(self.default, Exception):
                raise self.default from err
            return self.default

    def set_value(self, obj, value):
        try:
            obj[self.index] = value
            return
        except IndexError:
            while len(obj) < self.index+1:
                obj.append(None)
        obj[self.index] = value

    def del_value(self, obj):
        try:
            obj.pop(self.index)
        except IndexError:
            pass


list_property = ListProperty
