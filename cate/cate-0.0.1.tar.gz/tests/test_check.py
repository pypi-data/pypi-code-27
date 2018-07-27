# -*- coding: utf-8 -*-

from cate import check


TEST_MATRICES = {
    '2x3_fail_square': ((0, 1, 2), (3, 4, 5)),
    '3x3_fail_symmetric': ((-1, 0, -1), (-1, 0, 0), (-1, 0, 1)),
    '2x2_fail_diagonal': ((0, 0), (0, 2)),
    '4x4_fail_neighbors': ((3, 2, 2, 3), (2, 2, 2, 3), (2, 2, 3, 4), (3, 3, 4, 4)),
    '4x4_fail_final-position': ((0, 0, 0, -1), (0, 1, 0, 0), (0, 0, 0, -1), (-1, 0, -1, -1)),
    '2x2-0_fail_submatrix': ((0, 1), (1, 1)),
    '2x2-1_fail_submatrix': ((1, 2), (2, 2)),
    '2x2-2_fail_submatrix': ((-1, -1), (-1, -2)),
    '3x3_fail_submatrix': ((-1, -1, -1), (-1, -2, -2), (-1, -2, -3)),
    '4x4_fail_planarity': ((0, 0, 0, 0), (0, 1, 0, -1), (0, 0, 0, -1), (0, -1, -1, -1)),
    '2x2_ok': ((0, 0), (0, 1)),
    '4x4_ok': ((-1, -1, -1, -1), (-1, 0, 0, 0), (-1, 0, 1, 1), (-1, 0, 1, 2)),
}


def _build_test(check_, *, true_, false_):
    """
    Build a test case for a check function.

    - `check_` is  the name of the function to test.
    - `true_` is an iterable of keys of TEST_MATRICES keys for which `check_`
       should return `True`
    - `false_` is an iterable of keys of TEST_MATRICES keys for which `check_`
       should return `False`
    """
    def _test_function():
        for name in true_:
            assert check_(TEST_MATRICES[name])
        for name in false_:
            assert not check_(TEST_MATRICES[name])
    return _test_function


test_is_square = _build_test(  # pylint: disable=invalid-name
    check.is_square,
    true_=(
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x3_fail_square',
    ),
)

test_is_symmetric = _build_test(  # pylint: disable=invalid-name
    check.is_symmetric,
    true_=(
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '3x3_fail_symmetric',
    ),
)

test_diagonal_criterion = _build_test(  # pylint: disable=invalid-name
    check._diagonal_criterion,  # pylint: disable=protected-access
    true_=(
        '3x3_fail_symmetric',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x2_fail_diagonal',
    ),
)

test_neighbors_criterion = _build_test(  # pylint: disable=invalid-name
    check._neighbors_criterion,  # pylint: disable=protected-access
    true_=(
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
    ),
)

test_final_position_criterion = _build_test(  # pylint: disable=invalid-name
    check._final_position_criterion,  # pylint: disable=protected-access
    true_=(
        '2x2_fail_diagonal',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
    ),
)

test_is_continuous = _build_test(  # pylint: disable=invalid-name
    check.is_continuous,
    true_=(
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
    ),
)

test_submatrix_criterion = _build_test(  # pylint: disable=invalid-name
    check._submatrix_criterion,  # pylint: disable=protected-access
    true_=(
        '2x3_fail_square',
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_final-position',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '4x4_fail_neighbors',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
    ),
)

test_planarity_criterion = _build_test(  # pylint: disable=invalid-name
    check._planarity_criterion,  # pylint: disable=protected-access
    true_=(
        '2x2_fail_diagonal',
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '4x4_fail_planarity',
    ),
)

test_is_deterministic = _build_test(  # pylint: disable=invalid-name
    check.is_deterministic,
    true_=(
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
    ),
)

test_is_linking = _build_test(  # pylint: disable=invalid-name
    check.is_linking,
    true_=(
        '2x2_ok',
        '4x4_ok',
    ),
    false_=(
        '2x3_fail_square',
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
    ),
)
