# -*- coding: utf-8 -*-

"""
Core routines and optimization logic.
"""

from . import check


def final_position(matrix):
    """Compute the final position of strands according to the linking matrix."""
    assert check.is_symmetric(matrix)
    size = len(matrix)
    # compute the final order of strands using Melvin's algorithm
    # given a strand `s` and an index `i`, we have `final_order[i] == s`
    final_order = list(range(size))
    for i, row in enumerate(matrix):
        for j in range(i):  # decreasing index in final order
            if row[j] % 2 == 1:
                final_order[i] -= 1
        for j in range(i + 1, size):  # increasing index in final order
            if row[j] % 2 == 1:
                final_order[i] += 1
    # transform final_order to get the final position
    # given a strand `s` and an index `i`, we have `final_position_[s] == i`
    final_position_ = [None] * size
    for i, strand in enumerate(final_order):
        final_position_[strand] = i
    return final_position_
