dprops = [
    "ID",
    "Image",
    "Command",
    "CreatedAt",
    "RunningFor",
    "Ports",
    "Status",
    "Size",
    "Names",
    "Labels",
    "Mounts",
    "Networks"
]
class DockerData(object):
    def __init__(self, init_str, delimiter="¤"):
        for i, v in enumerate(init_str.split(delimiter)):
            setattr(self, property(dprops[i], v))

