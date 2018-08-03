import random


class Response:
    def __init__(self, text=None, emoji=None, ghostly=None, threaded=None):
        self.text = text
        self.emojis = emoji
        self.ghostly = ghostly
        self.threaded_response = threaded

    def respond(self, client, payload):
        if self.text:
            client.post_message(channel=payload.channel, message=self.get_response_value(self.text))
        if self.emojis:
            client.react(payload, self.get_response_value(self.emojis))
        if self.ghostly:
            client.ephemeral(payload, self.get_response_value(self.ghostly))
        if self.threaded_response:
            client.thread_reply(payload, self.get_response_value(self.threaded_response))

    @staticmethod
    def get_response_value(options):
        res = options
        if type(options) is list:
            res = random.choice(options)
        return res
