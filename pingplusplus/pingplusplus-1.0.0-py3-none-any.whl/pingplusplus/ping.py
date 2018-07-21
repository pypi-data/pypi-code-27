import time
import random
import struct
import select
import socket

def get_checksum(data):
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return struct.pack('<H', ~x & 0xFFFF)

def ping(addr, timeout=2, number=1, data=b''):
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    payload = struct.pack('!HH', random.randrange(0, 65536), number) + data

    try:
        conn.connect((addr, 80))
        conn.sendall(b'\x08\0' + get_checksum(b'\x08\0\0\0' + payload) + payload)
    except socket.gaierror:
        return timeout * 1000
        
    start = time.time()

    while select.select([conn], [], [], max(0, start + timeout - time.time()))[0]:
        data = conn.recv(65536)
        if len(data) < 20 or len(data) < struct.unpack_from('!xxH', data)[0]:
            continue
        if data[20:] == b'\0\0' + get_checksum(b'\0\0\0\0' + payload) + payload:
            return round(time.time() - start, 6) * 1000

    return timeout * 1000

def pingHasPermission():
  try:
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    return True
  except PermissionError:
    print('PermissionError: ping++ requires admin privileges to open raw socket')
    return False
