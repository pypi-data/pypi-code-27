#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import types
import unittest
from unittest import TestCase
import numpy as np
import sys
sys.path.append('../')
from fpq import numba_wrapper


def _identity_decorator(*args, **kwargs):
    if (len(args) == 1) and isinstance(args[0], types.FunctionType):
        return args[0]

    def wrapper(fn):
        return fn

    return wrapper


class TestNumbaWrapperWithoutNumba(TestCase):
    '''Tests numba_wrapper without the numba.'''
    @classmethod
    def setUpClass(cls):
        cls._old = (numba_wrapper.IS_ENABLED_NUMBA, numba_wrapper.jit)
        numba_wrapper.IS_ENABLED_NUMBA = False
        numba_wrapper.jit = _identity_decorator

    @classmethod
    def tearDownClass(cls):
        numba_wrapper.IS_ENABLED_NUMBA = cls._old[0]
        numba_wrapper.jit = cls._old[1]

    def test_IS_ENABLED_NUMBA(self):
        self.assertFalse(numba_wrapper.IS_ENABLED_NUMBA)

    def test_jit(self):
        @numba_wrapper.jit
        def func(x):
            pass

        self.assertTrue(isinstance(func, types.FunctionType))

    def test_avoid_non_supported_types(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_non_supported_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_non_supported_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_non_supported_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_non_supported_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        @numba_wrapper.avoid_non_supported_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float16)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float32)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float64)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

    def test_avoid_mapping_to_py_types(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_mapping_to_py_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_mapping_to_py_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        @numba_wrapper.avoid_mapping_to_py_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.float16(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float16))

        dataset = np.float32(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float32))

        dataset = np.float64(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float64))

    def test_chain_of_decorators(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types
                @numba_wrapper.avoid_non_supported_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types()
                @numba_wrapper.avoid_non_supported_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_mapping_to_py_types(0)
            @numba_wrapper.avoid_non_supported_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_mapping_to_py_types('y')
            @numba_wrapper.avoid_non_supported_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        @numba_wrapper.avoid_mapping_to_py_types
        @numba_wrapper.avoid_non_supported_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float16)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float32)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float64)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.float16(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float16))

        dataset = np.float32(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float32))

        dataset = np.float64(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float64))


@unittest.skipIf(not numba_wrapper.IS_ENABLED_NUMBA, 'Numba is not installed.')
class TestNumbaWrapperWithNumba(TestCase):
    '''Tests numba_wrapper with the numba.'''
    def test_IS_ENABLED_NUMBA(self):
        self.assertTrue(numba_wrapper.IS_ENABLED_NUMBA)

    def test_jit(self):
        @numba_wrapper.jit
        def func(x):
            pass

        self.assertTrue(isinstance(func, numba_wrapper.CPUDispatcher))

    def test_avoid_non_supported_types(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_non_supported_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_non_supported_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_non_supported_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_non_supported_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_non_supported_types
                @numba_wrapper.jit(nopython=True)
                def func(x):
                    return x

                func(np.float16(1))
            except:
                pass
            else:
                raise Exception

        @numba_wrapper.avoid_non_supported_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float16)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float32)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float64)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

    def test_avoid_mapping_to_py_types(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_mapping_to_py_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_mapping_to_py_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        @numba_wrapper.avoid_mapping_to_py_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.float16(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float16))

        dataset = np.float32(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float32))

        dataset = np.float64(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float64))

    def test_chain_of_decorators(self):
        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types
                @numba_wrapper.avoid_non_supported_types
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(Exception):
            try:
                @numba_wrapper.avoid_mapping_to_py_types()
                @numba_wrapper.avoid_non_supported_types()
                @numba_wrapper.jit
                def func(x):
                    pass
            except:
                pass
            else:
                raise Exception

        with self.assertRaises(TypeError):
            @numba_wrapper.avoid_mapping_to_py_types(0)
            @numba_wrapper.avoid_non_supported_types(0)
            @numba_wrapper.jit
            def func(x):
                pass

        with self.assertRaises(ValueError):
            @numba_wrapper.avoid_mapping_to_py_types('y')
            @numba_wrapper.avoid_non_supported_types('y')
            @numba_wrapper.jit
            def func(x):
                pass

        @numba_wrapper.avoid_mapping_to_py_types
        @numba_wrapper.avoid_non_supported_types
        @numba_wrapper.jit
        def func(x):
            return x

        self.assertTrue(isinstance(func, types.FunctionType))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float16)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float32)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.random.uniform(low=-1., high=1., size=10).astype(np.float64)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.ndarray))

        dataset = np.float16(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float16))

        dataset = np.float32(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float32))

        dataset = np.float64(1)
        actual = func(dataset)
        self.assertTrue(isinstance(actual, np.float64))
