# -*- coding: utf-8 -*-

"""
some help class/functions for client API.
"""

__all__ = ['CFunc', 'declare', 'IpcFunc', 'NetFunc']


def declare(funcs):
    """Decoration for :class:`CFunc`

    :param list funcs: The to-be-bind functions list

    Add the decorated :class:`CFunc` class into to-be-bind functions list
    """

    def wrapper(clz):
        """wrapper of the decorator
        """
        if not clz.added:
            funcs.append(clz)
            clz.added = True
        return clz

    return wrapper


# pylint: disable=R0903
class CFunc:
    """C-API function definition

    .. warning:: Can **NOT** be used for callback functions
    """
    added = False
    c_func = None  # type: function
    prefix = ''
    func_name = ''
    argtypes = []
    restype = None

    @classmethod
    def bind(cls, dll):
        """
        bind C library function into this python class
        """
        prefix = str(cls.prefix or '')
        func_name = str(cls.func_name or cls.__name__)
        cls.c_func = getattr(dll, '{0}{1}'.format(prefix, func_name))
        if cls.argtypes:
            cls.c_func.argtypes = cls.argtypes
        if cls.restype:
            cls.c_func.restype = cls.restype


# pylint: disable=R0903
class IpcFunc(CFunc):
    """Class for smartbus IPC client library
    """
    prefix = 'SmartBusIpcCli_'


# pylint: disable=R0903
class NetFunc(CFunc):
    """Class for smartbus network client library
    """
    prefix = 'SmartBusNetCli_'
