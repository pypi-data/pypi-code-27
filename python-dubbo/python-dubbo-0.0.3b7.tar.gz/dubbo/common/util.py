# -*- coding: utf-8 -*-
import os
import socket
import struct
import threading
from sys import platform, maxsize
from urlparse import urlparse, unquote, parse_qsl

ip = None
heartbeat_id = 0
invoke_id = 0

# 获取调用ID时必须要加锁
invoke_id_lock = threading.Lock()


def num_2_byte_list(num):
    """
    convert num to byte list
    :param num:
    :return:
    """
    byte = []
    while num > 0:
        b = num & 0xff  # 获取最低位的一个字节的值
        byte.append(b)
        num = num >> 8  # 移除最低位的一个字节
    return list(reversed(byte))


def byte_list_2_num(byte):
    """
    convert byte list to num
    :param byte:
    :return:
    """
    num = 0
    for b in byte:
        num += b
        num = num << 8
    num = num >> 8  # 将最后一次的移位恢复
    return num


def double_to_long_bits(value):
    """
    https://gist.github.com/carlozamagni/187e478f516cac926682
    :param value:
    :return:
    """
    if value != value:
        return 0x7ff8000000000000L
    else:
        return struct.unpack('Q', struct.pack('d', value))[0]


def get_ip():
    global ip
    if ip:
        return ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
    finally:
        sock.close()
    return ip


def get_pid():
    return os.getpid()


def is_linux():
    if platform == "linux" or platform == "linux2":
        return True
    else:
        return False


def parse_url(url_str):
    """
    把url字符串解析为适合于操作的对象
    :param url_str:
    :return:
    """
    url = urlparse(unquote(url_str))
    fields = dict(parse_qsl(url.query))
    result = {
        'scheme': url.scheme,
        'host': url.netloc,
        'hostname': url.hostname,
        'port': url.port,
        'path': url.path,
        'fields': fields
    }
    return result


def get_invoke_id():
    """
    获取dubbo的调用id
    :return:
    """
    global invoke_id
    invoke_id_lock.acquire()
    result = invoke_id
    invoke_id += 1
    if invoke_id == maxsize:
        invoke_id = 0  # 大于long的最大值则重置为0
    invoke_id_lock.release()
    return result


if __name__ == '__main__':
    pass
