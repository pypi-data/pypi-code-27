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

import sys
import click
import carbon_slack.config as c
import carbon_slack.relay as relay
import carbon_slack.slack as slack
import time
import datetime as dt

@click.command()
def init():
    """Print a sample configuration file"""
    c.serialized_sample()

@click.command()
@click.option('--config', '-c', help='Alternative config YAML')
def relay(config=None):
    """Start up a relay that reads metrics from plaintext Slack, and pushes to plaintext Carbon"""
    cfg = c.load(config)

    client = relay.Relay(cfg)
    try:
        while True:
            client.run()
            time.sleep(10)
    except KeyboardInterrupt:
        if client is not None:
            try:
                client.close()
            finally:
                print "attempted to close relay"

    sys.stderr.write("\nExiting\n")
    sys.exit(0)

@click.command()
@click.option('--config', '-c', help='Alternative config YAML')
def recv(config=None):
    """Receive metric messages coming from Slack plaintext messages.

    This is intended as a way to test Slack message sending.
    """
    cfg = c.load(config)

    recv = slack.Receiver(cfg)
    messages = recv.get_messages()
    for m in messages:
        username = recv.find_user(m['user'])
        m['username'] = username
        m['datestamp'] = dt.fromtimestamp(m['ts'])
        print "%(datestamp)s  %(username)s: %(text)s" % m

@click.command()
@click.argument('metric_name')
@click.argument('metric_value')
@click.option('--config', '-c', help='Alternative config YAML')
def send(args, config=None):
    """Command-line sender for metrics to Slack (using plaintext messages).

    This could be useful for testing a Slack connection, or for calling from 
    a shell script or similar, simple service.
    """
    cfg = c.load()

    sender = slack.Sender(cfg)
    now = int(time.time())
    sender.send("%s %s %s" % (args.metric_name, args.metric_value, now))
