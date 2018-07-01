# -*- coding: utf-8 -*-
""" OpenVPN management module """

__author__  = "Adrien DELLE CAVE <adc@doowan.net>"
__license__ = """
    Copyright (C) 2016  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import logging
import socket


LOG = logging.getLogger("sonicprobe.helpers")


class OpenVPNMgmt(object):
    def __init__(self, host, port, timeout = None, start_open = False):
        self._host      = host
        self._port      = port
        self._timeout   = timeout
        self._connected = False
        self._sock      = None
        self.eol        = '\r\n'

        if start_open:
            self.open()

    def open(self):
        if self._connected:
            return self

        self._sock      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self._timeout is not None:
            self._sock.settimeout(self._timeout)

        self._sock.connect((self._host, self._port))
        self.readline()
        self._connected = True

        return self

    def close(self):
        if not self._connected:
            return self

        self._connected = False
        self._sock.close()

        return self

    def writeline(self, data):
        LOG.debug("send: %r", data)
        return self._sock.send(data + self.eol)

    def readline(self):
        r = []
        s = 0

        while True:
            c = self._sock.recv(1)

            if c == '\r':
                s = 1
            elif s == 1:
                s = 0
                if c == '\n':
                    break
                r.append(c)
            else:
                r.append(c)

        return ''.join(r)

    def readlinesuntil(self, data = None, timeout = None):
        timeout_prev    = self._timeout

        if timeout is not None:
            self._sock.settimeout(timeout)

        def reader():
            while True:
                x   = self._sock.recv(4096)
                if x == '':
                    continue

                x   = x.strip()

                if x.find(data) > -1:
                    break
                yield x

        r = ''.join(reader())

        self._sock.settimeout(timeout_prev)

        return r

    def readuntil(self, data = None, timeout = None):
        if not data:
            size    = 1
        else:
            size    = len(data)

        timeout_prev    = self._timeout

        if timeout is not None:
            self._sock.settimeout(timeout)

        def reader():
            while True:
                tmp = self._sock.recv(size)
                if not tmp or (data and data == tmp):
                    break
                yield tmp

        r = ''.join(reader())

        self._sock.settimeout(timeout_prev)

        return r

    def kill(self, client):
        LOG.debug("kill: %r", client)

        self.writeline("kill %s" % client)
        rs  = self.readline()

        LOG.debug("result: %r", rs)

        return rs.split(':', 1)
