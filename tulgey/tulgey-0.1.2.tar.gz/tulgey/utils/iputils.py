import socket
from typing import List
import ipaddress

def isValidIPv6(address: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except socket.error:
        return False

def normalizeIPv6(address: str) -> str:
    return socket.inet_ntop(socket.AF_INET6, socket.inet_pton(socket.AF_INET6, address.strip()))

def isValidIPv4(address: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        return False

def isValidIPv4Range(ipRange: str) -> bool:
    return ipRange.count("/") == 1 and isValidIPv4(ipRange.split("/")[0])

def expandIPv4Range(ipRange: str) -> List[str]:
    net = ipaddress.ip_network(ipRange)
    ret = []
    for host in net.hosts():
        ret.append(host.exploded)
    return ret