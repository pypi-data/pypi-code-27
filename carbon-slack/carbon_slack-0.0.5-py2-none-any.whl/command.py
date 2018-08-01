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

import sys
import click
import carbon_slack.config
import carbon_slack.relay
import carbon_slack.slack
import time
import datetime

@click.command()
def init():
    """Print a sample configuration file"""
    carbon_slack.config.serialized_sample()

@click.command()
@click.option('--config-file', '-c', help='Alternative config YAML')
def relay(config_file=None):
    """Start up a relay that reads metrics from plaintext Slack, and pushes to plaintext Carbon"""
    cfg = carbon_slack.config.load(config_file)

    client = carbon_slack.relay.Relay(cfg)
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
@click.option('--config-file', '-c', help='Alternative config YAML')
def recv(config_file=None):
    """Receive metric messages coming from Slack plaintext messages.

    This is intended as a way to test Slack message sending.
    """
    cfg = carbon_slack.config.load(config_file)

    recv = carbon_slack.slack.Receiver(cfg)
    messages = recv.get_messages()
    for m in messages:
        username = recv.find_user(m['user'])
        m['username'] = username
        m['datestamp'] = datetime.fromtimestamp(m['ts'])
        print "%(datestamp)s  %(username)s: %(text)s" % m

@click.command()
@click.argument('metric_name')
@click.argument('metric_value')
@click.option('--config-file', '-c', help='Alternative config YAML')
def send(args, config_file=None):
    """Command-line sender for metrics to Slack (using plaintext messages).

    This could be useful for testing a Slack connection, or for calling from 
    a shell script or similar, simple service.
    """
    cfg = carbon_slack.config.load(config_file)

    sender = carbon_slack.slack.Sender(cfg)
    now = int(time.time())
    sender.send("%s %s %s" % (args.metric_name, args.metric_value, now))

