class Bool(object):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise ValueError
        self.value = value

    def __bool__(self):
        return self.value

    __nonzero__ = __bool__


base_types = {bool: Bool}
