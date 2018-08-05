from .palm import Palm
from .wrist import Wrist
from .fingers import Fingers

class Hand:
    def __init__(self, data):
        self.type = data['data']['type']
        self.palm = Palm(data)
        self.wrist = Wrist(data)
        self.fingers = Fingers(data)
