from .rotation import Rotation

class Wrist:
    def __init__(self, data):
        wrist = data['data']['wrist']
        self.data = wrist
        self.rotation = Rotation(*wrist['quat'][1:])
