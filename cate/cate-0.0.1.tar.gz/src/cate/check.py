# -*- coding: utf-8 -*-

"""
Logic to check the validity of linking matrices.
"""

import itertools

from . import core


def is_square(matrix):
    """Check whether matrix is square."""
    size = len(matrix)
    return all(len(row) == size for row in matrix)


def is_symmetric(matrix):
    """Check whether matrix is symmetric."""
    assert is_square(matrix)
    size = len(matrix)
    transpose_pairs = (
        (matrix[i][j], matrix[j][i])
        for i in range(size)
        for j in range(i)
    )
    return all(x == y for x, y in transpose_pairs)


def _diagonal_criterion(matrix):
    """Check whether neighbor elements on the diagonal differ by exactly one."""
    size = len(matrix)
    diagonal_pairs = (
        (matrix[i][i], matrix[i + 1][i + 1])
        for i in range(size - 1)
    )
    return all(x - y in (-1, 1) for x, y in diagonal_pairs)


def _neighbors_criterion(matrix):
    """Check whether neighbor elements in the matrix differ by at most one."""
    assert is_symmetric(matrix)
    size = len(matrix)
    orthogonal_pairs = (
        # checking verticals for the whole matrix is enough due to symmetry
        (matrix[i][j], matrix[i + 1][j])
        for i in range(size - 1)
        for j in range(size)
    )
    diagonal_pairs = (
        (matrix[i][j], matrix[i + 1][j + 1])
        # checking lower triangular matrix is enough due to symmetry
        for i in range(1, size - 1)  # ignore diagonal as it as already been checked
        for j in range(i)
    )
    antidiagonal_pairs = (
        (matrix[i][j], matrix[i - 1][j + 1])
        # checking lower triangular matrix is enough due to symmetry
        for i in range(2, size)
        for j in range(i - 1)
    )
    neighbor_pairs = itertools.chain(
        orthogonal_pairs,
        diagonal_pairs,
        antidiagonal_pairs
    )
    return all(x - y in (-1, 0, 1) for x, y in neighbor_pairs)


def _final_position_criterion(matrix):
    """Check whether the final position of strands is a genuine permutation."""
    size = len(matrix)
    return set(core.final_position(matrix)) == set(range(size))


def is_continuous(matrix):
    """Check whether the linking matrix is continuous, i.e. no strands are torn."""
    return (
        _diagonal_criterion(matrix)
        and _neighbors_criterion(matrix)
        and _final_position_criterion(matrix)
    )


def _submatrix_criterion(matrix):
    """Check adjacent strands overlap deterministically."""
    size = len(matrix)
    # A 2x2 submatrix | x y | is encoded as the tuple (x, y, z, t).
    #                 | z t |
    diagonal_submatrices = (
        (matrix[i][i], matrix[i][i + 1], matrix[i + 1][i], matrix[i + 1][i + 1])
        for i in range(size - 1)
    )
    # The presence of submatrices | -1 0 | or | 0  0 | (up to a constant
    #                             |  0 0 |    | 0 -1 |
    # additive factor) indicates a violation of determinism.  For a 2x2
    # submatrix encoded as the tuple (x, y, z, t), this is the case when:
    #     x + 1 == y == z == t or x == y == z == t + 1
    return not any(
        x + 1 == y == z == t or x == y == z == t + 1
        for x, y, z, t in diagonal_submatrices
    )


def _planarity_criterion(matrix):
    """Check whether the final position of strands is planar."""

    # We associate to each strand i two intervals: [i - 1, i] and [i, i + 1].
    # We only consider for strand 0 (resp. size - 1) the interval [0, 1]
    # (resp.  [size - 2, size - 1]).  Each interval is identified by its lower
    # (left) bound.
    #
    # The final position of the strands represents a sequence of intervals
    # opening/closing.  The first occurrence of interval i is an opening, the
    # second is a closing.
    #
    # Checking whether the final position of strands is planar is then
    # equivalent to check whether both the sequence of intervals with even
    # identifiers and the sequence of intervals with odd identifiers correspond
    # to a valid nesting of function calls (opening is a function call, closing
    # is a function return).  This is done with a sweep-line algorithm.

    def _intervals_sequence(final_position_, *, parity):
        """Generate the sequence of intervals with a given parity."""
        assert parity in (0, 1)
        for bound in final_position_:
            if bound % 2 == parity:
                if bound < len(final_position_) - 1:
                    yield bound  # open interval
            else:
                if bound > 0:
                    yield bound - 1  # close interval

    def _is_valid_intervals_sequence(sequence):
        """Check whether sequence represents a valid nesting of function calls."""
        history = set()  # set of already encountered intervals
        stack = []  # stack of active intervals (opened but no closed)
        for interval in sequence:
            if interval in history:
                try:
                    active_interval = stack.pop()
                except IndexError:
                    return False  # an already closed interval has been re-opened
                if interval != active_interval:
                    return False
            else:
                history.add(interval)
                stack.append(interval)
        return not bool(stack)  # all intervals must be closed

    final_position_ = core.final_position(matrix)
    even_intervals = _intervals_sequence(final_position_, parity=0)
    odd_intervals = _intervals_sequence(final_position_, parity=1)
    return (
        _is_valid_intervals_sequence(even_intervals)
        and _is_valid_intervals_sequence(odd_intervals)
    )


def is_deterministic(matrix):
    """Check whether the linking matrix is deterministic."""
    return (
        _submatrix_criterion(matrix)
        and _planarity_criterion(matrix)
    )


def is_linking(matrix):
    """Check whether the matrix is a valid linking matrix."""
    return (
        is_square(matrix)
        and is_symmetric(matrix)
        and is_continuous(matrix)
        and is_deterministic(matrix)
    )
