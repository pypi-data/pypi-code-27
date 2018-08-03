import logging

import time
from typing import List

from botworks.channel.Channel import Channel
from botworks.slack.Clack import Clack
from botworks.slack.MessageHandler import MessageHandler

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class Botworks:
    def __init__(self, bot_token, bot_name, channels: List[Channel], config=None):
        if config is None:
            config = {}
        self.botToken = bot_token
        self.botName = bot_name
        self.channels = channels
        self.conf = config
        if config and 'log_level' in config:
            log.setLevel(config['log_level'])
        for c in self.channels:
            for r in c.responses:
                r.finalize(self.conf)

    def listen(self):
        clacker = Clack(self.botToken, self.botName, config=self.conf)
        for c in self.channels:
            c.channelId = next(slack_channel for slack_channel in clacker.all_channels() if slack_channel['name'] and slack_channel['name'] == c.channelName)['id']
            for mod_name in c.mod_names:
                mod_user = clacker.find_user_by_name(mod_name)
                if mod_user and 'id' in mod_user:
                    c.mod_ids.append(mod_user['id'])

        message_handler = MessageHandler(clacker, channels=self.channels, config=self.conf)
        while True:
            try:
                message_handler.parse_slack_output(clacker.read())
                time.sleep(self.conf["sleep_time"])
            except Exception as e:
                log.error("Major error")
                log.error(e)
                time.sleep(self.conf["error_sleep_time"])
