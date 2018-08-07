# -*- coding: utf-8 -*-

"""
ctypes for network client API.
"""

from __future__ import absolute_import

from ctypes import c_int, c_void_p, c_char_p, c_byte, c_ushort

from .helper import NetFunc as ApiFunc, declare
from .mutual import *  # pylint: disable=W0401,W0614

__all__ = [
    'DLL_NAME', 'get_function_declarations',
    'Init', 'Release',
    'SetCallBackFn', 'SetCallBackFnArg', 'SetCallBackFnEx',
    'CreateConnect', 'SendData',
    'RemoteInvokeFlow', 'SendPing', 'SendNotify',
    'SetTraceStr'
]

#: Default so/dll name
DLL_NAME = 'busnetcli'

#: global C-API function wrapper class list
funcs = []  # pylint: disable=C0103


def get_function_declarations():
    """ 返回全局 C-API 函数列表

    :rtype: list
    """
    return funcs


@declare(funcs)
# pylint: disable=R0903
class Init(ApiFunc):
    """初始化
    """
    argtypes = [c_byte]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class Release(ApiFunc):
    """释放
    """
    pass


@declare(funcs)
# pylint: disable=R0903
class SetCallBackFn(ApiFunc):
    """设置回调
    """
    argtypes = [FNTYP_CONNECTION_CB, FNTYP_RECVDATA_CB,
                FNTYP_DISCONNECT_CB, FNTYP_INVOKEFLOW_RET_CB,
                FNTYP_GLOBAL_CONNECT_CB, c_void_p]


@declare(funcs)
# pylint: disable=R0903
class SetCallBackFnArg(ApiFunc):
    """设置回调参数
    """
    argtypes = [c_void_p]


@declare(funcs)
# pylint: disable=R0903
class SetCallBackFnEx(ApiFunc):
    """设置更多回调
    """
    argtypes = [c_char_p, c_void_p]


@declare(funcs)
# pylint: disable=R0903
class CreateConnect(ApiFunc):
    """建立连接
    """
    argtypes = [c_byte, c_int, c_char_p, c_ushort,
                c_char_p, c_ushort, c_char_p, c_char_p, c_char_p]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class SendData(ApiFunc):
    """发送数据
    """
    argtypes = [c_byte, c_byte, c_byte, c_int, c_int, c_int, c_void_p, c_int]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class RemoteInvokeFlow(ApiFunc):
    """启动流程
    """
    argtypes = [c_byte, c_int, c_int, c_char_p,
                c_char_p, c_int, c_int, c_char_p]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class SendPing(ApiFunc):
    """发送 Ping 数据
    """
    argtypes = [c_byte, c_int, c_int, c_int, c_void_p, c_int]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class SendNotify(ApiFunc):
    """发送通知
    """
    argtypes = [c_byte, c_int, c_int, c_char_p,
                c_char_p, c_int, c_int, c_char_p]
    restype = c_int


@declare(funcs)
# pylint: disable=R0903
class SetTraceStr(ApiFunc):
    """设置 ``Trace``
    """
    argtypes = [FNTYP_TRACE_STR_CB]
