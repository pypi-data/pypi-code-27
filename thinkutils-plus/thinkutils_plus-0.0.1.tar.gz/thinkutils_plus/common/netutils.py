#!/usr/bin/env python
#coding=utf-8

import socket
import fcntl
import struct

def get_hostname():
    return socket.gethostname()
# print get_hostname()

def get_ip_address(ifname = "eth0"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# def get_local_ip_address():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # doesn't even have to be reachable
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP
#
# print get_hostname()
# print get_local_ip_address()
# print get_ip_address("eth0")

