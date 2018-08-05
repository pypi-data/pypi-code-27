from .rotation import Rotation

class Thumb:
    def __init__(self, data):
        thumb = data['data']['fingers'][0]
        self.rotation = Rotation(*thumb['quat'][1:])
        self.bend = thumb['bend']


class Fingers:
    def __init__(self, data):
        index = data['data']['fingers'][1]
        middle = data['data']['fingers'][2]
        third = data['data']['fingers'][3]
        little = data['data']['fingers'][4]
        self.data = data['data']['fingers']
        self.thumb = Thumb(data)
        self.index = Rotation(pitch=index['ang'][0], yaw=index['ang'][1])
        self.middle = Rotation(pitch=middle['ang'][0], yaw=middle['ang'][1])
        self.third = Rotation(pitch=third['ang'][0], yaw=third['ang'][1])
        self.little = Rotation(pitch=little['ang'][0], yaw=little['ang'][1])
