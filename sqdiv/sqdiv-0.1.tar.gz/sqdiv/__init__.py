import numpy as np


def divisors(x: int):
    """
    Returns the divisors of x, up to the square root of x.
    """
    divs = []
    upperbound = int(np.round(np.sqrt(x)))

    for i in range(1, upperbound + 1):
        if x % i == 0:
            divs.append(i)
    return divs


def n_rows_cols(x: int, squared: bool=False):
    """
    Returns the 'squarest' divisors of x.

    The 'squarest' divisors of x are defined as the divisors of x that are
    closest together on the number line.

    Prime numbers are automatically assigned to the next largest square.

    :param x: The integer to split into rows and columns.
    :param squared: Whether to go for a squarer layout or not.
    """
    divs = divisors(x)
    isprime = len(divs) == 1 and divs[0] == 1
    if squared or isprime:
        nrows = int(np.ceil(np.sqrt(x)))
        ncols = nrows
    else:
        nrows = max(divisors(x))
        ncols = int(x / nrows)
    return nrows, ncols
