from fractions import Fraction
import unittest

# import pytest

from claptrap.backports import choices, suppress


# class SomeError(Exception):
#     '''some error'''


# class SomeOtherError(Exception):
#     '''some other error'''


# def test_suppress_normal():
#     with backports.suppress(SomeError):
#         raise SomeError()

# def test_suppress_wrong_exc():
#     with pytest.raises(SomeOtherError):

### copypasta https://github.com/python/cpython/blob/dd0e087edc/Lib/test/test_contextlib.py#L992
class TestSuppress(unittest.TestCase):

    # @support.requires_docstrings
    # def test_instance_docs(self):
    #     # Issue 19330: ensure context manager instances have good docstrings
    #     cm_docstring = suppress.__doc__
    #     obj = suppress()
    #     self.assertEqual(obj.__doc__, cm_docstring)

    def test_no_result_from_enter(self):
        with suppress(ValueError) as enter_result:
            self.assertIsNone(enter_result)

    def test_no_exception(self):
        with suppress(ValueError):
            self.assertEqual(pow(2, 5), 32)

    def test_exact_exception(self):
        with suppress(TypeError):
            len(5)

    def test_exception_hierarchy(self):
        with suppress(LookupError):
            "Hello"[50]

    def test_other_exception(self):
        with self.assertRaises(ZeroDivisionError):
            with suppress(TypeError):
                1 / 0

    def test_no_args(self):
        with self.assertRaises(ZeroDivisionError):
            with suppress():
                1 / 0

    def test_multiple_exception_args(self):
        with suppress(ZeroDivisionError, TypeError):
            1 / 0
        with suppress(ZeroDivisionError, TypeError):
            len(5)

    def test_cm_is_reentrant(self):
        ignore_exceptions = suppress(Exception)
        with ignore_exceptions:
            pass
        with ignore_exceptions:
            len(5)
        with ignore_exceptions:
            with ignore_exceptions:  # Check nested usage
                len(5)
            outer_continued = True
            1 / 0
        self.assertTrue(outer_continued)


class TestBasicOps(unittest.TestCase):
    # gen = random.Random()

    ### copypasta https://github.com/python/cpython/blob/dd0e087edc/Lib/test/test_random.py#L153
    def test_choices(self):
        # choices = self.gen.choices
        data = ["red", "green", "blue", "yellow"]
        str_data = "abcd"
        range_data = range(4)
        set_data = set(range(4))

        # basic functionality
        for sample in [
            choices(data, k=5),
            choices(data, range(4), k=5),
            choices(k=5, population=data, weights=range(4)),
            choices(k=5, population=data, cum_weights=range(4)),
        ]:
            self.assertEqual(len(sample), 5)
            self.assertEqual(type(sample), list)
            self.assertTrue(set(sample) <= set(data))

        # test argument handling
        with self.assertRaises(TypeError):  # missing arguments
            choices(2)

        self.assertEqual(choices(data, k=0), [])  # k == 0
        self.assertEqual(
            choices(data, k=-1), []
        )  # negative k behaves like ``[0] * -1``
        with self.assertRaises(TypeError):
            choices(data, k=2.5)  # k is a float

        self.assertTrue(
            set(choices(str_data, k=5)) <= set(str_data)
        )  # population is a string sequence
        self.assertTrue(
            set(choices(range_data, k=5)) <= set(range_data)
        )  # population is a range
        with self.assertRaises(TypeError):
            choices(set_data, k=2)  # population is not a sequence

        self.assertTrue(set(choices(data, None, k=5)) <= set(data))  # weights is None
        self.assertTrue(set(choices(data, weights=None, k=5)) <= set(data))
        with self.assertRaises(ValueError):
            choices(data, [1, 2], k=5)  # len(weights) != len(population)
        with self.assertRaises(TypeError):
            choices(data, 10, k=5)  # non-iterable weights
        with self.assertRaises(TypeError):
            choices(data, [None] * 4, k=5)  # non-numeric weights
        for weights in [
            [15, 10, 25, 30],  # integer weights
            [15.1, 10.2, 25.2, 30.3],  # float weights
            [
                Fraction(1, 3),
                Fraction(2, 6),
                Fraction(3, 6),
                Fraction(4, 6),
            ],  # fractional weights
            [True, False, True, False],  # booleans (include / exclude)
        ]:
            self.assertTrue(set(choices(data, weights, k=5)) <= set(data))

        with self.assertRaises(ValueError):
            choices(data, cum_weights=[1, 2], k=5)  # len(weights) != len(population)
        with self.assertRaises(TypeError):
            choices(data, cum_weights=10, k=5)  # non-iterable cum_weights
        with self.assertRaises(TypeError):
            choices(data, cum_weights=[None] * 4, k=5)  # non-numeric cum_weights
        with self.assertRaises(TypeError):
            choices(
                data, range(4), cum_weights=range(4), k=5
            )  # both weights and cum_weights
        for weights in [
            [15, 10, 25, 30],  # integer cum_weights
            [15.1, 10.2, 25.2, 30.3],  # float cum_weights
            [
                Fraction(1, 3),
                Fraction(2, 6),
                Fraction(3, 6),
                Fraction(4, 6),
            ],  # fractional cum_weights
        ]:
            self.assertTrue(set(choices(data, cum_weights=weights, k=5)) <= set(data))

        # Test weight focused on a single element of the population
        self.assertEqual(choices("abcd", [1, 0, 0, 0]), ["a"])
        self.assertEqual(choices("abcd", [0, 1, 0, 0]), ["b"])
        self.assertEqual(choices("abcd", [0, 0, 1, 0]), ["c"])
        self.assertEqual(choices("abcd", [0, 0, 0, 1]), ["d"])

        # Test consistency with random.choice() for empty population
        with self.assertRaises(IndexError):
            choices([], k=1)
        with self.assertRaises(IndexError):
            choices([], weights=[], k=1)
        with self.assertRaises(IndexError):
            choices([], cum_weights=[], k=5)
