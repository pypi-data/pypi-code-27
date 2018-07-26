from . import hermit
from . import video
import requests
import datetime
from . import errors

def getHermit(name):
    rq = requests.get("http://hermitcraft.com/api/hermit/{}".format(name))
    if (rq.text == '{"Message":"An error has occurred."}'):
        raise(errors.InvaildHermitName("The Hermit Name '{}' is invalid".format(name)))
    else:
        return hermit.Hermit(rq.json())

def getVideos(type="Latest",member=None,start=None):
    if (start == None):
        start = datetime.datetime.utcnow()
    if member != None:
        url = "http://hermitcraft.com/api/videos?type={}&member={}&start={}".format(type,member,start.strftime("%a, %d %b %Y %H:%M:%S UTC"))
    else:
        url = "http://hermitcraft.com/api/videos?type={}&start={}".format(type, start.strftime("%a, %d %b %Y %H:%M:%S UTC"))
    rq = requests.get(url)

    videos = []

    for r in rq.json():
        videos.append(video.Video(r))
    return videos

def getLatestVideos():
    return getVideos(type="Latest")
def getAllVideos():
    return getVideos(type="All")
def getHermitcraftVideos():
    return getVideos(type="HermitCraft")

