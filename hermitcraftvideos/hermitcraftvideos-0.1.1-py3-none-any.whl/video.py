from . import hermit
import datetime
import requests

class Video():
    def __init__(self,data):
        self.title = data["title"]
        self.author = hermit.Hermit(data["uploader"])
        self.hermit = self.author

        self.id = data["id"]

        self.likes = data["likeCount"]
        self.comments = data["commentCount"]
        self.views = data["viewCount"]

        self.uploaded = data["uploaded"]
        self.uploaded_time = data["uploadedFriendly"]
        self.uploaded_short = data["uploadedFriendlyMobile"]

        self.duration = data["duration"]
        self.duration_time = data["friendlyDuration"]

        self.thumbnail = "http://i.ytimg.com/vi/{}/mqdefault.jpg".format(self.id)
    def update(self):
        rq = requests.get("http://hermitcraft.com/api/videostats?id={}".format(self.id))
        data = rq.json()[self.id]
        self.likes = data["likeCount"]
        self.comments = data["commentCount"]
        self.views = data["viewCount"]
