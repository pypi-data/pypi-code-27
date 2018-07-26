import requests
import datetime
from . import video

class Hermit:
    def __init__(self,data):
        self._load(data)
    def _load(self,data):
        self.active = data["Active"]
        self.name = data["ChannelName"]
        self.displayname = data["DisplayName"]

        self.website = data["WebsiteURL"]
        self.googleplus = data["GooglePlusLink"]
        self.picture = data["ProfilePicture"]

        self.live = data["Streaming"]

        if data["TwitterName"] == None:
            self.twitter = None
        else:
            self.twitter = HermitTwitter(data["TwitterName"])

        if data["ChannelName"] == None:
            self.youtube = None
        else:
            self.youtube = HermitYoutube(data["ChannelName"],data["YTStreaming"])

        if data["BeamName"] == None:
            self.mixer = None
            self.beam = self.mixer
        else:
            self.mixer = HermitMixer(data["BeamName"],data["BeamStreaming"])
            self.beam = self.mixer

        if data["TwitchName"] == None:
            self.twitch = None
        else:
            self.twitch = HermitTwitch(data["TwitchName"],data["Streaming"])
    def update(self):
        rq = requests.get("http://hermitcraft.com/api/hermit/{}".format(self.name))
        self._load(rq.json())
    def getVideos(self):
        rq = requests.get("http://hermitcraft.com/api/hermitvideos?type=Latest&member={}&start={}".format(self.name,datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")))
        data = rq.json()
        videos = []
        for d in data:
            videos.append(video.Video(d))
        return videos

class HermitTwitter:
    def __init__(self,name):
        self.name = name
        self.url = "https://twitter.com/{}".format(name)

class HermitYoutube:
    def __init__(self,name,live):
        self.name = name
        self.url = "https://www.youtube.com/user/{}".format(name)
        self.live = live

class HermitMixer:
    def __init__(self,name,live):
        self.name = name
        self.url = "https://mixer.com/{}".format(name)
        self.live = live

class HermitTwitch:
    def __init__(self,name,live):
        self.name = name
        self.url = "https://www.twitch.tv/{}".format(name)
        self.live = live