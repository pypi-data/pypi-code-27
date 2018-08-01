# This file is part of Carbon-Slack.
#
# Carbon-Slack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Carbon-Slack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Carbon-Slack.  If not, see <https://www.gnu.org/licenses/>.

import socket

class PlaintextSender(object):
    def __init__(self, config):
        """Initialize a new Carbon sender that will use the plaintext protocol for sending metrics"""
        self.config = config

    def close(self):
        """If a socket is open for sending data at the time when the user kills this script, try to close it 
        gracefully.
        """
        if self.sock is not None:
            self.sock.close()

    def send_metrics(self, metrics):
        """Serialize the metrics dict (of the form k:v without timestamps) along with a generated timestamp into a
        multi-line payload. Then, send it over a new socket to the Carbon daemon.
        """
        self.sock = socket.socket()
        conn_info = (self.config.carbon_server, self.config.carbon_port)
        try:
            print("Connecting to: %s:%d" % conn_info)
            self.sock.connect(conn_info)
            
            for line in metrics:
                print("Sending:\n%s\n" % line)
                self.sock.send(line + "\n")
        except socket.error:
            raise SystemExit("Couldn't connect to %s:%d, is carbon-cache.py running?" % conn_info)

        finally:
            if self.sock is not None:
                print("Attempting to close socket.")
                self.sock.close()
                self.sock = None

