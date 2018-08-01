#!/usr/bin/env python

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

import carbon_slack.config as conf
from carbon_slack.slack import Receiver
import sys
import time

config = {
	conf.TOKEN: sys.argv[1],
	conf.CHANNEL: sys.argv[2] if len(sys.argv) > 2 else None
}

recv = Receiver(config)

while True:
	messages = recv.get_messages()
	for m in messages:
		print m

	recv.ack_messages([m['ts'] for m in messages])
	time.sleep(1)

# for c in recv.list_channels():
# 	print "%s (%s)" % (c['name'], c['id'])