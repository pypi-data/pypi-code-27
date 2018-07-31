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

import time
import socket
from carbon_slack.slack import Receiver
from carbon_slack.carbon import PlaintextSender

class Relay(object):
    def __init__(self, config, last_message=0):
        """Initialize the Relay using a config dict and an optional last-message timestamp (in unix seconds).
        """
        self.recv = Receiver(config, last_message)
        self.send = PlaintextSender(config)
        self.config = config

    def close(self):
        """If a socket is open in the sender at the time when the user kills this script, try to close it 
        gracefully.
        """
        self.send.close()

    def run(self):
        """Receive any available messages from the Slack channel and assume they are metrics triplets (key, value, tstamp).
        Messages can be multi-line, with a triplet per line. For each message that we can parse in this way,
        add the message 'ts' value to an acks array, which will be used to delete those messages from the 
        Slack channel to reduce the possibility of duplicate processing.

        For each triplet we can parse, send a new metric data point over a socket that we open to the Carbon
        daemon for this purpose, using newline-delimited plaintext.
        """
        messages = self.recv.get_messages()
        if len(messages) < 1:
            print "No metrics to report"
            return 0

        print "Sending stats..."

        acks = []
        metrics = []
        for m in messages:
            lines = [l.rstrip() for l in m['text'].splitlines()]
            for line in lines:
                parts = line.split(' ')
                if len(parts) < 3:
                    continue

                metrics.append("%s %s %s\n" % (parts[0], parts[1], parts[2]))
            acks.append(m['ts'])

        if len(acks) > 0:
            self.sender.send_metrics(metrics)
            self.recv.ack_messages(acks)

        return len(acks)

