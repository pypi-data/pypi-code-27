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

from ruamel.yaml import YAML
import getpass
import subprocess
import os
import sys

CONFIG_PATH = '/etc/carbon-slack.yml'

TOKEN = 'token'
CHANNEL = 'channel'
CARBON_SERVER='carbon-server'
CARBON_PORT='carbon-port'

class Config(object):
    def __init__(self, data):
        """Create a configuration instance suitable for use with the Carbon-Slack relay (and associated commands).

        NOTE: This could be created from an external YAML (or dict) source, and doesn't have to be read from the 
        CONFIG_PATH (/etc/carbon-slack.yml by default).
        """
        self.token = data[TOKEN]
        self.channel = data[CHANNEL]
        self.carbon_server = data[CARBON_SERVER]
        self.carbon_port = data[CARBON_PORT]

def serialized_sample():
    """Serialize a sample configuration to STDOUT"""
    return YAML().dump({
        TOKEN: 'xoxp-1234567890-yadda-yadda',
        CHANNEL: 'metrics',
        CARBON_SERVER: '127.0.0.1',
        CARBON_PORT: 2023
    }, sys.stdout)

def load(config_file=None):
    """Load a Carbon-Slack relay configuration from a YAML file (by default, use /etc/carbon-slack.yml)"""
    config_path = config_file or CONFIG_PATH
    data = {}

    with open(config_path) as f:
        data = YAML().load(f)

    return Config(data)


