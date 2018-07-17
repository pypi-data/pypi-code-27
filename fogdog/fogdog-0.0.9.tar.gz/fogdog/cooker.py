from .logger import logger


__all__ = ['cooker']


# --------------------------------
# Decorator
# For registering cookers
# --------------------------------
class Cooker(object):

    def __init__(self):
        self._cookers = {}

    def __call__(self, name):
        if not self._is_name_valid(name):
            raise ValueError('cooker name already exists! name = %s' % name)

        def wrapper(func):
            self._cookers[name] = func
            return func
        return wrapper

    def _is_name_valid(self, name):
        if name in self._cookers.keys():
            return False
        return True

    def getattr(self, name):
        if name in self._cookers.keys():
            return self._cookers[name]
        else:
            raise ValueError('Cooker is not registered! name = %s' % name)


cooker = Cooker()
# --------------------------------


def cook(data, cooker_name, spices=None):
    """ Cook data.

    :param data: iterable rows
    :param cooker_name: cooker name
    :param spices: tuple
    :return: list of rows
    """
    logger.info("cooker: %s" % cooker_name)
    if not spices:
        spices = ()
    if not isinstance(spices, tuple):
        raise ValueError('spices must be tuple!')

    return [cooker.getattr(cooker_name)(row, *spices) for row in data]


# --------------------------------
# Registered cookers.
# --------------------------------

@cooker('MoveSum')
def move_sum(row, aggregate=1, skip=1):
    if aggregate == 1 and skip == 1:
        return row
    m = (len(row) - aggregate) // skip + 1
    return [sum((row[i * skip: i * skip + aggregate])) for i in range(m)]


