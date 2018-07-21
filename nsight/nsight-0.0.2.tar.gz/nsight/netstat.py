import os
from collections import namedtuple
from subprocess import check_output
from .config import DATA_DIR

NMAP_SERVICES_PATH = os.path.join(DATA_DIR, 'nmap-services.txt')
PORTMAP = {}


PortMapping = namedtuple('PortMapping', 'name port proto')
NetstatLine = namedtuple('NetstatLine', 'proto recvq sendq local_ip local_port '
                         'foreign_ip foreign_port state pid prog local_name '
                         'foreign_name')


def _parse_portmap_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    name, port_proto = line.split()[:2]
    port, proto = port_proto.split('/')
    return PortMapping(
        name=name,
        port=int(port),
        proto=proto,
    )


def _convert_port(p):
    if p.isdigit():
        return int(p)
    else:
        return p


def load_portmap():
    if PORTMAP:
        return
    with open(NMAP_SERVICES_PATH) as f:
        for line in f:
            pm = _parse_portmap_line(line)
            if pm is None:
                continue
            PORTMAP[pm.proto, pm.port] = pm.name


def netstat(use_sudo=False):
    load_portmap()
    cmd = ['netstat', '--ip', '-pltn']
    if use_sudo:
        cmd = ['sudo'] + cmd
    out = check_output(cmd).decode('utf8')
    netstats = []
    for line in out.splitlines():
        spl = line.split()
        proto = spl[0]
        if proto not in ['tcp', 'udp']:
            continue
        recvq = spl[1]
        sendq = spl[2]
        local_ip, local_port = spl[3].split(':')
        local_port = _convert_port(local_port)
        local_name = None
        if isinstance(local_port, int):
            local_name = PORTMAP.get((proto, local_port))
        foreign_ip, foreign_port = spl[4].split(':')
        foreign_port = _convert_port(foreign_port)
        foreign_name = None
        if isinstance(foreign_port, int):
            foreign_name = PORTMAP.get((proto, foreign_port))
        state = spl[5]
        pid_prog = spl[6]
        if pid_prog and pid_prog != '-':
            pid, prog = pid_prog.split('/', 1)
        else:
            pid, prog = None, None
        nsl = NetstatLine(
            proto=proto,
            recvq=int(recvq),
            sendq=int(sendq),
            local_ip=local_ip,
            local_port=local_port,
            foreign_ip=foreign_ip,
            foreign_port=foreign_port,
            state=state,
            pid=int(pid) if pid is not None else None,
            prog=prog,
            local_name=local_name,
            foreign_name=foreign_name,
        )
        netstats.append(nsl)
    return netstats


def print_netstat(netstats):
    if not netstats:
        print('nothing being served')
        return
    for ns in netstats:
        local_name = ns.local_name or 'unknown'
        s_port = '{} ({})'.format(ns.local_port, local_name)
        if ns.local_ip == '0.0.0.0':
            s_to = 'all'
        elif ns.local_ip == '127.0.0.1':
            s_to = 'local'
        else:
            s_to = ns.local_ip
        s_pid = 'from unknown process'
        if ns.pid:
            s_pid = 'from PID {} ({})'.format(ns.pid, ns.prog)
        print('listening on port {} serving to {} {}'.format(
            s_port, s_to, s_pid,
        ))
