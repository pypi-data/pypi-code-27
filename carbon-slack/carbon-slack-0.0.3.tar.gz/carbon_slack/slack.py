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

import slackclient as client
import time

def find_channel_id(slack, name):
    """Allow a user to configure this system using a user-friendly channel name.
    The network handlers will use this method to map that to a channel ID.
    """
    result = slack.api_call("channels.list", exclude_members=True)
    for channel in result['channels']:
        if channel['name'] == name:
            return channel['id']

        prev_names = channel.get('previous_names')
        if prev_names is not None and name in prev_names:
            return channel['id']

    return None

class SlackBase(object):
    def __init__(self, config):
        """Setup fields common to all Slack-oriented service objects"""
        self.config = config
        self.slack = client.SlackClient(config.token)

        self.channel_id = find_channel_id(self.slack, config.channel)
        if self.channel_id is not None:
            self.slack.api_call('channels.join', channel=self.channel_id)

    def list_channels(self):
        """List the available Slack channels."""
        result = self.slack.api_call("channels.list")
        return [channel for channel in result['channels']]

    def find_user(self, user_id):
        """Lookup the user information for the given user id. Things like username will be available this way.
        """
        result = self.slack.api_call('users.info', user=user_id, include_locale=False)
        return result.get('user')

class Receiver(object):
    def __init__(self, config, last_message=0):
        """Construct a new Slack channel message receiver using the given configuration dict and an
        optional last-message timestamp (unix seconds).
        """
        super(SlackBase,self).__init__()
        self.last_message = last_message

    def get_last_seen_message(self):
        """Return the last-seen message after zero or more messages have been processed. This Receiver
        will keep track of the last-seen timestamp as it receives messages, such that the calling
        application can store this value and use it when restarting the script later.
        """
        return self.last_message

    def get_messages(self):
        """Receive any available messages on the Slack channel, and update the last-message timestamp
        appropriately before returning the array of message objects.
        """
        result = self.slack.api_call('channels.history', channel=self.channel_id, oldest=self.last_message)
        self.last_message=int(time.time())

        messages = result.get('messages') or []
        messages = messages[::-1]

        return messages

    def ack_messages(self, messages_ts):
        """Acknowledge that processing is complete for an array of messages (given by their 'ts' values in messages_ts).
        This acknowledgement happens by way of deleting the messages out of the channel to prevent duplicate processing.
        """
        if messages_ts is not None:
            for ts in messages_ts:
                self.slack.api_call('chat.delete', channel=self.channel_id, ts=ts)

class Sender(SlackBase):
    def __init__(self, config):
        """Construct a new Slack channel message sender using the given configuration dict to specify a token and 
        channel name.
        """
        super(SlackBase,self).__init__()

    def send_metrics(self, metrics):
        """Serialize the given metrics dict (assumed to be key:value pairs without timestamps) to triplets in a 
        multi-line message, using a timestamp generated in this method. Once the message is formatted, send it to 
        the configured Slack channel.
        """
        now = int(time.time())

        lines = []
        for k in metrics.keys():
            v = metrics[k]
            lines.append("%s %s %s" % (k, v, now))

        self.send("\n".join(lines))

    def send(self, message):
        """Send a simple string message to the configured Slack channel."""
        return self.slack.api_call('chat.postMessage', channel=self.channel_id, text=message)
