# This file is part of Carbon-Slack.

# Carbon-Slack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Carbon-Slack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

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
        try:
            self.sock.connect( (self.config.carbon_server, self.config.carbon_port) )
            
            output = "\n".join(metrics)
            print( "Sending:\n%s" % output)
            sock.send(output)
        except socket.error:
            raise SystemExit("Couldn't connect to %(server)s on port %(port)d, is carbon-cache.py running?" % 
                { 'server':self.config.carbon_server, 'port':self.config.carbon_port })

        finally:
            self.sock.close()
            self.sock = None

