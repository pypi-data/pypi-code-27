from .rotation import Rotation

class Speed:
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

class Palm:
    def __init__(self, data):
        palm = data['data']['palm']
        self.data = palm
        self.rotation = Rotation(*palm['quat'][1:])
        self.speed = Speed(*palm['spd'])
        self.acceleration = Speed(*palm['acc'])
