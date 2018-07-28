#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import types
import functools
import inspect
import numpy as np


try:
    from numba.targets.registry import CPUDispatcher
    from numba import jit

    IS_ENABLED_NUMBA = True

except ImportError:
    import warnings
    warning_text = \
        '\n\n' + '!' * 79 + '\n' + \
        'Could not import from numba.\n' + \
        'If numba is not installed, performance can be degraded in some functions.' + \
        '\n' + '!' * 79 + '\n'
    warnings.warn(warning_text)

    def _identity_decorator(*args, **kwargs):
        if (len(args) == 1) and isinstance(args[0], types.FunctionType):
            return args[0]

        def wrapper(fn):
            return fn

        return wrapper

    jit = _identity_decorator

    IS_ENABLED_NUMBA = False


def avoid_mapping_to_py_types(name_or_function=None):
    '''Avoid mapping to Python types.'''
    if name_or_function is None:
        is_omitted = True
        func = None
    elif isinstance(name_or_function, str):
        is_omitted = False
        func = None
    elif isinstance(name_or_function, types.FunctionType) \
            or (IS_ENABLED_NUMBA and isinstance(name_or_function, CPUDispatcher)):
        is_omitted = True
        func = name_or_function
    else:
        raise TypeError('Type {} is not supported.'.format(type(name_or_function)))

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ret = fn(*args, **kwargs)
            if isinstance(ret, (np.ndarray, np.float16)):
                return ret
            else:
                return args[index].dtype.type(ret)

        if is_omitted:
            index = 0
        else:
            sig = inspect.signature(fn)
            index = list(sig.parameters.keys()).index(name_or_function)

        return wrapper if IS_ENABLED_NUMBA else fn

    return decorator if func is None else decorator(func)


def avoid_non_supported_types(name_or_function=None):
    '''Avoid non-supported types.'''
    if name_or_function is None:
        is_omitted = True
        func = None
    elif isinstance(name_or_function, str):
        is_omitted = False
        func = None
    elif isinstance(name_or_function, types.FunctionType) \
            or (IS_ENABLED_NUMBA and isinstance(name_or_function, CPUDispatcher)):
        is_omitted = True
        func = name_or_function
    else:
        raise TypeError('Type {} is not supported.'.format(type(name_or_function)))

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if args[index].dtype == np.float16:
                return fn.py_func(*args, **kwargs)
            else:
                return fn(*args, **kwargs)

        if is_omitted:
            index = 0
        else:
            sig = inspect.signature(fn)
            index = list(sig.parameters.keys()).index(name_or_function)

        return wrapper if IS_ENABLED_NUMBA else fn

    return decorator if func is None else decorator(func)
