
class Channel:
    def __init__(self, name, mod_names, responses):
        self.channelName = name
        self.mod_names = mod_names
        self.responses = responses
        self.channelId = None
        self.mod_ids = []
