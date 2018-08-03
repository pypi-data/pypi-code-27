from .robottypes import is_integer


def roundup(number, ndigits=0, return_type=None):
    """Rounds number to the given number of digits.

    Numbers equally close to a certain precision are always rounded away from
    zero. By default return value is float when ``ndigits`` is positive and
    int otherwise, but that can be controlled with ``return_type``.

    With the built-in ``round()`` rounding equally close numbers as well as
    the return type depends on the Python version.
    """
    sign = 1 if number >= 0 else -1
    precision = 10 ** (-1 * ndigits)
    if not return_type:
        return_type = float if ndigits > 0 else int
    quotient, remainder = divmod(abs(number), precision)
    if (remainder >= precision / 2):
        quotient += 1
    return sign * return_type(quotient * precision)


def plural_or_not(item):
    count = item if is_integer(item) else len(item)
    return '' if count == 1 else 's'